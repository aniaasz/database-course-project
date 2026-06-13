from datetime import datetime
import re # obsługuje wyrażenia regularne - wygodne sprawdzanie maila i telefonu
"""
^ - początek linii
? - wystąpienie 0 lub 1 razy
+ - co najmniej jedno wystąpienie
* - co najmniej 0 wystąpień
[] - zestaw dozwolonych znaków
{} - liczba powtórzeń lub zakres
$ - koniec linii
"""


# funkcje pomocnicze

def validate_email(email):
    """
    Sprawdza, czy podany adres e-mail ma poprawny format (np. test@domena.pl).
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return False
    return True


def validate_phone(phone):
    """
    Sprawdza czy telefon ma od 9 do 15 znaków i składa się z cyfr i ewentualnie plusa
    """
    # usuwanie spacji i myślników
    phone_num = phone.replace(" ", "").replace("-", "")

    phone_regex = r'^\+?[0-9]{9,15}$'
    if not re.match(phone_regex, phone_num):
        return False
    return True


#     Zbiór funkcji do walidacji danych
#     Zwracają krotkę (True, "") jeśli wszystko jest ok, lub (False, "komunikat błędu")

def validate_customer_data(first_name, last_name, email, phone):
    """
    Walidacja danych klienta
    """
    # .strip() usuwa spacje z początku i końca
    if len(first_name.strip()) < 2:
        return False, "First name must be at least 2 characters long."

    if len(last_name.strip()) < 2:
        return False, "Last name must be at least 2 characters long."

    if not validate_email(email):
        return False, "Invalid email format"

    if not validate_phone(phone):
        return False, "Invalid phone format"

    return True, ""


def validate_book_data(price):
    """
    Sprawdza czy cena książki jest dodatnia
    """
    try:
        val_price = float(price)
        if val_price <= 0:
            return False, "Price must be greater than 0 PLN"
        return True, ""
    except ValueError:
        return False, "Price must be a number"


def validate_storage_data(in_stock, discount, base_price=None):
    """
    Sprawdza stan magazynowy oraz poprawność rabatu
    """
    try:
        val_stock = int(in_stock)
        val_discount = float(discount)

        if val_stock < 0:
            return False, "Stock quantity cannot be negative"

        if val_discount < 0:
            return False, "Discount cannot be negative"

        if base_price is not None and val_discount > float(base_price):
            return False, "Discount cannot be higher than the book's base price"

        return True, ""
    except ValueError:
        return False, "Stock must be an integer and discount must be a number."


def validate_release_date(date_string):
    """
    Sprawdza czy data ma poprawny format (YYYY-MM-DD) oraz czy nie jest z przyszłości
    """
    try:
        # datetime.strptime automatycznie sprawdza poprawność dni w miesiącu
        parsed_date = datetime.strptime(date_string, "%Y-%m-%d").date()
        current_date = datetime.now().date()

        if parsed_date > current_date:
            return False, "Date cannot be in the future"

        return True, ""
    except ValueError:
        return False, "Invalid date format - expected YYYY-MM-DD"