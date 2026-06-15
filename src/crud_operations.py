import pymysql

from db_config import get_connection


# OPERACJE: CREATE

def register_client(imie, nazwisko, adres, telefon, email):
    """
    Rejestruje nowego klienta w bazie danych
    Zwraca ID nowo utworzonego klienta
    """
    # with automatycznie zamknie połączenie z bazą po zakończeniu funkcji
    with get_connection() as connection:
        # kursor pozwala na przesyłanie i wykonywanie SQL
        with connection.cursor() as cur:
            sql = """
                INSERT INTO Customers (first_name, last_name, address, phone, email)
                VALUES (%s, %s, %s, %s, %s)
            """

            cur.execute(sql, (imie, nazwisko, adres, telefon, email))

            # cursor.lastrowid  - pobranie automatycznie wygenerowanego ID
            nowe_id = cur.lastrowid

            connection.commit()

            print(f"Registered new customer with ID: {nowe_id}")
            return nowe_id


def create_book(tytul, autor, gatunek, wydawnictwo, data_wydania, cena):
    """
    Dodaje nową książkę do ogólnego katalogu (tabela Books)
    Zwraca ID nowo dodanej książki
    """
    with get_connection() as connection:
        with connection.cursor() as cur:
            sql = """
                INSERT INTO Books (title, author, genre, publisher, release_date, price)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cur.execute(sql, (tytul, autor, gatunek, wydawnictwo, data_wydania, cena))
            nowe_id = cur.lastrowid
            connection.commit()

            print(f"Added book to catalogue with ID: {nowe_id}")
            return nowe_id


def add_book_to_storage(id_ksiazki, stan_produktu, ilosc, rabat):
    """
    Przypisuje książkę z katalogu do fizycznego magazynu (tabela Storage)
    z określeniem jej stanu (new/used/damaged) ilości oraz ewentualnego rabatu
    """
    with get_connection() as connection:
        with connection.cursor() as cur:
            sql = """
                INSERT INTO Storage (book_id, `condition`, in_stock, discount)
                VALUES (%s, %s, %s, %s)
            """
            # Słowo 'condition' w MySQL jest słowem zastrzeżonym
            # dlatego zapisane jest jako `condition`
            cur.execute(sql, (id_ksiazki, stan_produktu, ilosc, rabat))
            connection.commit()

            print(f"Added book ID {id_ksiazki} to storage (Condition: {stan_produktu}, Quantity: {ilosc})")


# OPERACJE: READ

def get_outlet_books(condition):
    """
    Pobiera listę książek z kategorii outlet na podstawie podanego stanu
    :param condition: Tekst 'used' lub 'damaged'
    """
    if condition not in ['used', 'damaged']:
        raise ValueError("Condition must be either 'used' or 'damaged'")

    with get_connection() as connection:
        # DictCursor zwraca dane jako słownik gdzie kluczami są nazwy kolumn z bazy danych
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            sql = """
                SELECT b.title, b.author, b.genre, b.publisher, s.condition, 
                       (b.price - s.discount) AS price_with_discount 
                FROM Books b
                JOIN Storage s ON s.book_id = b.id
                WHERE s.condition = %s AND s.in_stock > 0
            """

            cur.execute(sql, (condition,))
            results = cur.fetchall()
            print(f"Found {len(results)} outlet books with condition: '{condition}'")
            return results


def get_regular_books():
    """
    Pobiera listę nowych książek
    """
    with get_connection() as connection:
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            sql = """
                SELECT b.title, b.author, b.genre, b.publisher, s.condition, b.price 
                FROM Books b
                JOIN Storage s ON s.book_id = b.id
                WHERE s.condition = 'new' AND s.in_stock > 0
            """
            cur.execute(sql)
            results = cur.fetchall()
            print(f"Found {len(results)} regular books")
            return results


def get_all_books():
    """
    Pobiera wszystkie książki
    """
    with get_connection() as connection:
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            sql = """
                SELECT b.title, b.author, b.genre, s.condition, 
                       COALESCE(b.price - s.discount, b.price) AS price
                FROM Books b
                JOIN Storage s ON s.book_id = b.id
                WHERE s.in_stock > 0
            """
            cur.execute(sql)
            results = cur.fetchall()
            print(f"Found {len(results)} regular books")
            return results


def get_customer_by_name(first_name, last_name):
    """
    Wyświetla podstawowe dane klienta
    """
    with get_connection() as connection:
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            sql = """SELECT first_name, last_name, address, phone, email FROM Customers 
            WHERE first_name = %s AND last_name = %s"""
            cur.execute(sql, (first_name, last_name))
            res = cur.fetchone()

            if not res:
                print(f"Customer {first_name} {last_name} not found")
            return res


def search_books(cond):
    """
    Wyświetla książki o danym tytule lub danego autora
    """
    with get_connection() as connection:
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            sql = """SELECT b.id, b.title, b.author, b.genre, b.publisher, b.price, s.condition FROM Books b 
            JOIN Storage s ON s.book_id = b.id WHERE b.title LIKE %s OR b.author LIKE %s"""
            cur.execute(sql, (f"%{cond}%", f"%{cond}%"))
            res = cur.fetchall()

            if not res:
                print(f"Books not found")
            return res


def get_customer_order_history(customer_id):
    """
    Pobiera pełną historię zamówień dla jednego konkretnego klienta na podstawie jego ID
    """
    with get_connection() as connection:
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            sql = """
                SELECT o.id AS order_id, c.first_name, c.last_name, b.title, b.author, s.condition, o.order_date, od.quantity, od.price 
                FROM Customers c
                JOIN Orders o ON c.id = o.customer_id
                JOIN Order_Details od ON od.order_id = o.id
                JOIN Storage s ON s.id = od.storage_id
                JOIN Books b ON b.id = s.book_id
                WHERE c.id = %s
            """
            cur.execute(sql, (customer_id,))
            results = cur.fetchall()
            print(f"Found {len(results)} order history items for customer ID: {customer_id}")
            return results


# OPERACJE: UPDATE

def update_customer_contact(customer_id, field_name, new_value):
    """
    Dynamicznie zmienia jedno wybrane pole tekstowe klienta
    """
    # zabezpieczenie przed modyfikacją nieistniejących kolumn
    allowed_fields = ['first_name', 'last_name', 'address', 'phone', 'email']
    if field_name not in allowed_fields:
        raise ValueError(f"Field {field_name} is not allowed to be updated")

    with get_connection() as connection:
        with connection.cursor() as cur:
            sql = f"UPDATE Customers SET {field_name} = %s WHERE id = %s"
            cur.execute(sql, (new_value, customer_id))
            connection.commit()
            print(f"Updated {field_name} to '{new_value}' for customer ID {customer_id}")


def restock_storage(storage_id, quantity_to_add):
    """
    Obsługuje dostawę towaru - zwiększa liczbę sztuk w magazynie o podaną wartość
    """
    with get_connection() as connection:
        with connection.cursor() as cur:
            sql = "UPDATE Storage SET in_stock = in_stock + %s WHERE id = %s"
            cur.execute(sql, (quantity_to_add, storage_id))
            connection.commit()
            print(f"Added {quantity_to_add} units to storage item ID {storage_id}")


def decrease_storage_stock(storage_id, quantity_to_remove):
    """
    Obsługuje zakup książki - zmniejsza stan magazynowy pod warunkiem że jest wystarczająca ilość
    Zwraca True jeśli transakcja się udała, lub False jeśli brakło towaru
    """
    with get_connection() as connection:
        with connection.cursor() as cur:
            sql = "UPDATE Storage SET in_stock = in_stock - %s WHERE id = %s AND in_stock >= %s"
            affected_rows = cur.execute(sql, (quantity_to_remove, storage_id, quantity_to_remove))
            connection.commit()

            # affected_rows - liczba zmodyfikowanych wierszy
            # jeśli 0 to znaczy że warunek nie został spełniony
            if affected_rows > 0:
                print(f"Successfully sold {quantity_to_remove} units from storage item ID {storage_id}")
                return True
            else:
                print(
                    f"Cannot sell {quantity_to_remove} units from storage item ID {storage_id} - insufficient stock")
                return False


def update_storage_discount(storage_id, new_discount):
    """
    Zmienia lub nakłada nową wartość rabatu dla danej pozycji w magazynie
    """
    with get_connection() as connection:
        with connection.cursor() as cur:
            sql = "UPDATE Storage SET discount = %s WHERE id = %s"
            cur.execute(sql, (new_discount, storage_id))
            connection.commit()
            print(f"Updated discount to {new_discount} for storage item ID {storage_id}")


def move_book_to_outlet(storage_id, new_condition, discount=0):
    """
    Zmienia status książki i nakłada ewentualną promocję
    """
    if new_condition not in ['used', 'damaged']:
        raise ValueError("Outlet condition is not valid")

    with get_connection() as connection:
        with connection.cursor() as cur:
            sql = "UPDATE Storage SET `condition` = %s, discount = %s WHERE id =%s"
            cur.execute(sql, (new_condition, discount, storage_id))
            connection.commit()
            print(f"Moved storage item {storage_id} to outlet")


# OPERACJE: DELETE

def delete_storage_item(storage_id):
    """
    Usuwa książkę z magazynu ale tylko wtedy gdy nikt jej jeszcze nie zamówił
    Operacja się nie powiedzie jeśli książka była kiedyś zamawiana
    """
    with get_connection() as connection:
        with connection.cursor() as cur:
            try:
                sql = "DELETE FROM Storage WHERE id = %s"
                affected_rows = cur.execute(sql, (storage_id,))
                connection.commit()

                if affected_rows > 0:
                    print(f"Successfully removed storage item ID {storage_id}")
                    return True
                else:
                    print(f"No storage item found with ID {storage_id}")
                    return False

            except pymysql.err.IntegrityError:
                # jeśli książka była zamawiana to zostanie złapany błąd
                print(f"Cannot delete storage item ID {storage_id} - it is linked to order history")
                return False


def cancel_order(order_id):
    """
    Anuluje całe zamówienie
    Najpierw usuwa rekordy z tabeli Order_Details a następnie usuwa główne zamówienie z tabeli Orders
    """
    with get_connection() as connection:
        with connection.cursor() as cur:
            # usuwanie szczegółów zamówienia
            sql_details = "DELETE FROM Order_Details WHERE order_id = %s"
            cur.execute(sql_details, (order_id,))

            # usuwanie głównego zamówienia
            sql_order = "DELETE FROM Orders WHERE id = %s"
            affected_rows = cur.execute(sql_order, (order_id,))

            connection.commit()

            if affected_rows > 0:
                print(f"Successfully cancelled order ID {order_id} and its details")
                return True
            else:
                print(f"No order found with ID {order_id}")
                return False


def delete_customer(customer_id):
    """
    Usuwa konto klienta z bazy danych
    Operacja się nie powiedzie jeśli klient posiada już jakąś historię zamówień
    """
    with get_connection() as connection:
        with connection.cursor() as cur:
            try:
                sql = "DELETE FROM Customers WHERE id = %s"
                affected_rows = cur.execute(sql, (customer_id,))
                connection.commit()

                if affected_rows > 0:
                    print(f"Successfully deleted customer ID {customer_id}")
                    return True
                else:
                    print(f"No customer found with ID {customer_id}")
                    return False
            except pymysql.err.IntegrityError:
                print(f"Cannot delete customer ID {customer_id} - this customer has placed orders in the past")
                return False
