from flask import Flask, jsonify, request
from flask_cors import CORS
from transaction_logic import process_order
import sys

from crud_operations import (
    get_customer_by_name, get_customer_order_history, update_customer_contact,
    get_regular_books, get_outlet_books, get_all_books,
    delete_storage_item, register_client, add_book_to_storage, create_book
)
from reports import (
    get_top_selling_books, get_loyalty_report, get_low_stock_status, get_sales_analysis
)

# inicjalizacja aplikacji
app = Flask(__name__)
# aby front w JS w działał i przeglądarka nie blokowała połączenia
CORS(app)


# -----------------ENDPOINTY DLA KLIENTA

# pobiera historię zamówień dla danego klienta
@app.route('/api/customer/<int:customer_id>/history', methods=['GET'])
def api_customer_history(customer_id):
    try:
        # pobranie danych z bazy na podstawie przesłanego w adresie ID
        history = get_customer_order_history(customer_id)
        return jsonify(history), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# szuka klienta na podstawie imienia i nazwiska
@app.route('/api/customer/search', methods=['GET'])
def api_search_customer():
    # pobranie parametrów z paska adresu URL
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')

    try:
        customer = get_customer_by_name(first_name, last_name)
        if customer:
            return jsonify(customer), 200
        else:
            return jsonify(None), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# aktualizuje dane konkretnego klienta
@app.route('/api/customer/<int:customer_id>/update', methods=['POST'])
def api_update_customer(customer_id):
    # dane pobrane w formacie json przez fetch
    data = request.get_json()

    try:
        # dla każdego pola updatujemy jego wartość
        for field, new_value in data.items():
            update_customer_contact(customer_id, field, new_value)

        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------ENDPOINTY DLA KSIĄŻEK

# pobiera tylko nowe książki
@app.route('/api/books/regular', methods=['GET'])
def api_regular_books():
    try:
        books = get_regular_books()
        return jsonify(books), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# pobiera książki z outletu na podstawie stanu (używane / zniszczone)
@app.route('/api/books/outlet/<string:condition>', methods=['GET'])
def api_outlet_books(condition):
    try:
        books = get_outlet_books(condition)
        return jsonify(books), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# pobiera wszystkie książki dostępne w bazie
@app.route('/api/books/all', methods=['GET'])
def api_all_books():
    try:
        books = get_all_books()
        return jsonify(books), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# TOP 3 najlepiej sprzedające się książki
@app.route('/api/books/bestsellers', methods=['GET'])
def api_get_bestsellers():
    try:
        # pobieramy raport najlepiej sprzedających się książek ustawiając limit na 3
        bestsellery = get_top_selling_books(limit=3)
        return jsonify(bestsellery), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ------------------ENDPOINT STATYSTYK

# zbiera i updateuje statystyki wyświetlane na stronie głównej
@app.route('/api/stats', methods=['GET'])
def api_get_stats():
    from db_config import get_connection
    import pymysql

    try:
        with get_connection() as connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cur:
                # wszystkie dostępne tytuły
                cur.execute("SELECT COUNT(id) AS total_titles FROM Books")
                res_titles = cur.fetchone()

                # ilość książek w outlecie
                cur.execute("""SELECT COUNT(id) AS total_outlet FROM Storage
                            WHERE `condition` IN ('used', 'damaged') AND in_stock > 0""")
                res_outlet = cur.fetchone()

                # liczba zamówień
                cur.execute("SELECT COUNT(id) AS total_orders FROM Orders")
                res_orders = cur.fetchone()

                return jsonify({
                    "titles": res_titles['total_titles'] if res_titles else 0,
                    "outlet": res_outlet['total_outlet'] if res_outlet else 0,
                    "orders": res_orders['total_orders'] if res_orders else 0
                }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------ENDPOINTY DLA ADMINA

# dodawanie nowej książki i wrzucanie jej na magazyn
@app.route('/api/admin/books/add', methods=['POST'])
def api_admin_add_book():
    data = request.get_json()
    try:
        book_id = create_book(
            tytul=data.get('title'),
            autor=data.get('author'),
            gatunek=data.get('genre'),
            wydawnictwo=data.get('publisher'),
            data_wydania=data.get('release_date'),
            cena=float(data.get('price'))
        )
        add_book_to_storage(
            id_ksiazki=book_id,
            stan_produktu=data.get('condition'),
            ilosc=int(data.get('in_stock')),
            rabat=float(data.get('discount', 0))
        )
        return jsonify({"status": "success"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# rejestracja nowego klienta
@app.route('/api/admin/customers/add', methods=['POST'])
def api_admin_add_customer():
    data = request.get_json()
    try:
        customer_id = register_client(
            imie=data.get('first_name'),
            nazwisko=data.get('last_name'),
            adres=data.get('address'),
            telefon=data.get('phone'),
            email=data.get('email')
        )
        return jsonify(customer_id), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# usuwanie książki z magazynu
@app.route('/api/admin/books/delete/<int:storage_id>', methods=['DELETE'])
def api_admin_delete_book(storage_id):
    try:
        res = delete_storage_item(storage_id)
        if res:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# wyciąga raport analizy sprzedazy
@app.route('/api/admin/reports/sales-analysis', methods=['GET'])
def api_report_sales():
    try:
        return jsonify(get_sales_analysis()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# wyciąga raport niskiego stanu magazynoweog
@app.route('/api/admin/reports/low-stock/<int:limit>', methods=['GET'])
def api_report_low_stock(limit):
    try:
        return jsonify(get_low_stock_status(limit)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# wyciąga raport top 5 klientów
@app.route('/api/admin/reports/loyalty', methods=['GET'])
def api_report_loyalty():
    try:
        return jsonify(get_loyalty_report()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    #Domyślne dane 
    DEFAULT_CUSTOMER_ID = 1
    DEFAULT_ITEMS = [
        {'storage_id': 1, 'quantity': 1},
        {'storage_id': 2, 'quantity': 2}
    ]
    
    # Sprawdzamy, czy uruchamiamy skrypt z argumentami (do prezentacji w terminalu)
    if len(sys.argv) > 1:
        #przykładowe uruchomienie:
        #python main.py process_order 1 2
        try:
            nazwa_funkcji = sys.argv[1]# Pierwszy argument po nazwie pliku to nazwa funkcji, np. "process_order"
            if nazwa_funkcji == "process_order":
                # Jeśli podano ID klienta w konsoli, użyj go, inaczej bierzemy domyślne.
                customer_id = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_CUSTOMER_ID
                # Jeśli podano ID zamówienia (storage_id) w konsoli, tworzymy dla niego koszyk, inaczej domyślny koszyk
                if len(sys.argv) > 3:
                    storage_id = int(sys.argv[3])
                    items = [{'storage_id': storage_id, 'quantity': 1}]
                else:
                    items = DEFAULT_ITEMS

                print(f"Wykonuje dla klienta ID: {customer_id}")
                print(f"Zawartosc koszyka: {items}")
                # Wywołanie transakcji
                order_id = process_order(customer_id, items)
                if order_id:
                    print(f"SUKCES! Transakcja zapisana. ID zamowienia: {order_id}")
                else:
                    print("BLAD! Transakcja odrzucona (sprawdz stan magazynowy).")
            else:
                print(f"Nieznana funkcja: {nazwa_funkcji}. Dostepne: process_order")

        except Exception as e:
            print(f"Wystapil blad podczas prezentacji: {e}")   
    else: # Jeśli ktoś odpali program bez argumentów (zwykłe python main.py)
        # uruchomienie aplikacji w trybie debug aby łatwiej wyłapywać błędy
        # serwer słucha na porcie 5000
        print("Uruchamiam serwer Flask na porcie 5000...")
        app.run(debug=True, port=5000)
