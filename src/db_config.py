import os
import pymysql
from dotenv import load_dotenv


# Wczytanie zmiennych środowiskowych z pliku .env do pamięci aplikacji
# Dzięki temu możemy bezpiecznie pobierać hasła i dane dostępowe
load_dotenv()


def get_connection():
    """
        Funkcja tworząca i zwracająca nowe połączenie z bazą danych MySQL
        Wykorzystuje bibliotekę PyMySQL oraz konfigurację pobraną z pliku .env
    """
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        # Wymuszenie bezpiecznego szyfrowania połączenia (SSL).
        # Chmura Aiven domyślnie odrzuca nieszyfrowane połączenia.
        # Przekazanie pustego słownika {} włącza domyślny SSL.
        ssl={}
    )
