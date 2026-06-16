import pymysql
from db_config import get_connection

def process_order(customer_id, items):
    """
    Proces Zakupu (Złożona transakcja bazodanowa).
    Wykonuje pełny cykl zamówienia w jednej transakcji z blokadą wierszy (obsługa współbieżności).
    
    :param customer_id: ID klienta składającego zamówienie (int)
    :param items: Lista słowników z koszykiem zakupowym, np.:
                  [
                     {'storage_id': 1, 'quantity': 2, 'price': 39.99},
                     {'storage_id': 4, 'quantity': 1, 'price': 24.50}
                  ]
    :return: ID utworzonego zamówienia w przypadku sukcesu, False w przypadku błędu.
    """
    with get_connection() as connection:
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            try:
                customer_id = int(customer_id)
                total_amount = 0
                
                #Sortowanie koszyka po ID zapobiega zakleszczeniom (deadlocks), gdy klienci kupują te same rzeczy naraz.
                items = sorted(items, key=lambda item: int(item['storage_id']))

                # Blokada (FOR UPDATE) dla sprawdzanych pozycji.
                # Zabezpiecza przed problemem race conditions przy równoległych zamówieniach.
                for item in items:
                    storage_id = int(item['storage_id'])
                    quantity_needed = int(item['quantity'])
                    
                    #Zmieniamy zapytanie, żeby pobierało bezpieczną cenę prosto z bazy danych (JOIN z Books), zamiast tego co w JSON, bo to może zostać zhackowane przez użytkownika
                    #dlatego cenę pobieramy bezpośrednio z bazy w momencie składania zamówienia
                    sql_lock = """
                        SELECT s.in_stock, s.`condition`, s.discount, b.price 
                        FROM Storage s 
                        JOIN Books b ON s.book_id = b.id 
                        WHERE s.id = %s FOR UPDATE
                    """
                    cur.execute(sql_lock, (storage_id,))
                    result = cur.fetchone()

                    # Walidacja dostępności stanu magazynowego
                    if not result or result['in_stock'] < quantity_needed:
                        raise Exception(f"Insufficient stock for storage ID: {storage_id}")
                    
                    # Wyliczenie autentycznej ceny po ewentualnych rabatach
                    real_price = float(result['price']) - float(result['discount'] or 0) #trzeba jeszcze uwzglednić rabat ewentualny
                    # Zapisuje bezpieczną cenę do słownika, żeby druga pętla mogła jej użyć
                    item['price'] = real_price
                    total_amount += (quantity_needed * real_price)

                # Utworzenie głównego rekordu zamówienia (nagłówka)
                sql_order = "INSERT INTO Orders (customer_id, order_date, total_amount) VALUES (%s, NOW(), %s)"
                cur.execute(sql_order, (customer_id, total_amount))
                order_id = cur.lastrowid

                # Zapisanie poszczególnych pozycji zamówienia
                for item in items:
                    storage_id = int(item['storage_id'])
                    quantity = int(item['quantity'])
                    price = float(item['price']) # Teraz to bezpiecznie pobiera real_price

                    sql_details = """
                        INSERT INTO Order_Details (order_id, storage_id, quantity, price) 
                        VALUES (%s, %s, %s, %s)
                    """
                    cur.execute(sql_details, (order_id, storage_id, quantity, price))
                    
                    # Dekrementacja fizycznego stanu magazynowego
                    sql_update_stock = "UPDATE Storage SET in_stock = in_stock - %s WHERE id = %s"
                    cur.execute(sql_update_stock, (quantity, storage_id))

                # Zatwierdzenie całej transakcji (commit zwalnia również blokady wierszy)
                connection.commit()
                return order_id

            except Exception as e:
                # Zastosowanie zasady all-or-nothing: wycofanie wszystkich operacji w przypadku błędu
                connection.rollback()
                print(f"Transaction failed: {e}")
                return False
