from flask import Flask, jsonify, request
from flask_cors import CORS


from crud_operations import (
    get_customer_by_name, get_customer_order_history, update_customer_contact,
    get_regular_books, get_outlet_books, get_all_books
)

# inicjalizacja aplikacji
app = Flask(__name__)
# aby front w JS w działał i przeglądarka nie blokowała połączenia
CORS(app)


# ENDPOINTY DLA KLIENTA

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


# ENDPOINTY DLA KSIĄŻEK


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


# ENDPOINT STATYSTYK


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


if __name__ == '__main__':
    # uruchomienie aplikacji w trybie debug aby łatwiej wyłapywać błędy
    # serwer słucha na porcie 5000
    app.run(debug=True, port=5000)
