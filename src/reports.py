import pymysql
from database import get_connection

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
                ORDER BY suma_spent DESC
                -- Ograniczamy wynik tylko do 5 rekordów
                LIMIT 5
            """
            cur.execute(sql)
            return cur.fetchall()

"""Status magazynowy (Alert niskiego stanu)
Wyszukuje pozycje, których liczba sztuk w magazynie spadła poniżej podanej wartości X.Dzięki temu menedżer wie, co trzeba pilnie domówić."""
def get_low_stock_status(limit_x):
    
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
