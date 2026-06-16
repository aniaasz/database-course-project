import pymysql
from db_config import get_connection

"""Analiza sprzedaży.
Łączy szczegóły zamówień z magazynem, grupuje po stanie książki i sumuje przychód (ilość * cena) osobno dla 'new', 'used' i 'damaged'."""
def get_sales_analysis():
    with get_connection() as connection:
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            sql = """
                SELECT s.condition AS stan_ksiazki, 
                       SUM(od.quantity * od.price) AS laczny_przychod
                FROM Order_Details od
                -- Łączymy z tabelą Storage, żeby dowiedzieć się, w jakim stanie była sprzedana książka
                JOIN Storage s ON od.storage_id = s.id
                GROUP BY s.condition
            """
            cur.execute(sql)
            return cur.fetchall()

"""Raport "lojalnościowy" klientów (kto ile wydał)
Łączy klientów z ich zamówieniami, sumuje wydane kwoty, sortuje od największej wartości i zwraca TOP 5 najlepszych klientów."""
def get_loyalty_report():
    with get_connection() as connection:
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            sql = """
                SELECT c.first_name, c.last_name, 
                       SUM(o.total_amount) AS suma_wydana
                FROM Customers c
                -- JOIN łączy zamówienia z konkretnymi klientami
                JOIN Orders o ON c.id = o.customer_id
                GROUP BY c.id, c.first_name, c.last_name
                -- Sortujemy malejąco (DESC), czyli od tych, co wydali najwięcej
                ORDER BY suma_wydana DESC
                -- Ograniczamy wynik tylko do 5 rekordów
                LIMIT 5
            """
            cur.execute(sql)
            return cur.fetchall()

"""Status magazynowy (Alert niskiego stanu)
Wyszukuje pozycje, których liczba sztuk w magazynie spadła poniżej podanej wartości X.Dzięki temu menedżer wie, co trzeba pilnie domówić."""
def get_low_stock_status(limit_x):
    limit_x = int(limit_x)
    with get_connection() as connection:
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            sql = """
                SELECT b.title AS tytul, b.author AS autor, 
                       s.condition AS stan, s.in_stock AS dostepna_ilosc
                FROM Books b
                -- Łączymy katalog książek z fizycznym magazynem
                JOIN Storage s ON b.id = s.book_id
                -- Filtrujemy tylko te pozycje, gdzie stan magazynowy jest mniejszy niż limit_x
                WHERE s.in_stock < %s
                -- Sortujemy od tych, których brakuje najbardziej
                ORDER BY s.in_stock ASC
            """
            cur.execute(sql, (limit_x,))
            return cur.fetchall()
"""Całkowite zyski księgarni.
Sumuje całkowity historyczny przychód ze wszystkich zrealizowanych pozycji zamówień."""
def get_total_profits():
    with get_connection() as connection:
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            sql = """
                SELECT SUM(total_amount) AS total_profit
                FROM Orders
            """
            cur.execute(sql)
            # Fetchone because this query returns exactly one row with one sum value
            return cur.fetchone()


"""Najczęściej kupowane tytuły (Bestsellery).
Zlicza łączną liczbę sprzedanych egzemplarzy dla każdego tytułu i zwraca najpopularniejsze."""
def get_top_selling_books(limit=5):
    limit = int(limit)
    with get_connection() as connection:
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            sql = """
                SELECT b.title, b.author, SUM(od.quantity) AS total_sold
                FROM Order_Details od
                JOIN Storage s ON od.storage_id = s.id
                JOIN Books b ON s.book_id = b.id
                GROUP BY b.id, b.title, b.author
                ORDER BY total_sold DESC
                LIMIT %s
            """
            cur.execute(sql, (limit,))
            return cur.fetchall()

"""Aktualny stan magazynowy (Pełny wykaz).
Pokazuje wszystkie dostępne książki w magazynie (ilość > 0) z podziałem na ich stan."""
def get_full_warehouse_stock():
    
    with get_connection() as connection:
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            sql = """
                SELECT b.title, b.author, s.condition, s.in_stock
                FROM Books b
                JOIN Storage s ON b.id = s.book_id
                WHERE s.in_stock > 0
                ORDER BY b.title ASC, s.condition ASC
            """
            cur.execute(sql)
            return cur.fetchall()
