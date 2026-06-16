# Mini-projekt 📂


## 🫂 Autorzy:
Marta Komar, Anna Sznajder

## 📜 Opis
Księgarnia internetowa, w której użytkownicy mogą kupować książki w dwóch głównych kategoriach:
* **Regularne (Nowe):** Fabrycznie nowe książki w standardowych cenach.
* **Outlet:** Książki lekko uszkodzone lub używane, sprzedawane ze zniżką.

Aplikacja to pełnoprawny system Full-Stack z podziałem na role (Klient / Administrator), systemem raportowym oraz zarządzaniem stanami magazynowymi.

## 💻 Technologie
Backend: Python, Flask, PyMySQL

Baza danych: MySQL

Frontend: HTML, JavaScript

## 🚀 Funkcjonalności

### Dla Klienta:
* **Przeglądanie katalogu:** Podział asortymentu na książki nowe oraz outletowe (używane, zniszczone).
* **Dynamiczna wyszukiwarka:** Możliwość szybkiego wyszukiwania książek po tytule lub autorze.
* **Profil Użytkownika:** Podgląd profilu klienta z dynamicznym formularzem umożliwiającym edycję danych kontaktowych.
* **Historia Zamówień:** Szczegółowy wykaz zrealizowanych zakupów z automatycznie przeliczanymi kwotami i tłumaczeniem stanów fizycznych książek.

### Dla Administratora (Panel Admina):
* **Zarządzanie asortymentem (CRUD):** Dodawanie nowych tytułów do bazy oraz przypisywanie ich do fizycznego magazynu, wraz z bezpiecznym usuwaniem asortymentu.
* **Rejestracja klientów:** Dodawanie nowych użytkowników do systemu.
* **System Raportowy:**
  * Analiza przychodów wg stanu książek.
  * Raport lojalnościowy (TOP 5 klientów z największą sumą zamówień).
  * Alert krytycznych stanów magazynowych (wyszukiwanie braków asortymentu).

---

## ⚙️ Zaawansowane mechaniki bazodanowe i architektoniczne
Projekt został zbudowany z zachowaniem profesjonalnych praktyk inżynieryjnych:
* **Transakcje i reguły ACID:** Zastosowanie mechanizmów blokowania (`FOR UPDATE`) oraz kontroli transakcji (`connection.rollback()` i `commit()`) w celu zapobiegania "race conditions" podczas modyfikacji danych.
* **Ochrona przed SQL Injection:** Pełna parametryzacja zapytań bazodanowych (wykorzystanie `%s` przy przekazywaniu danych wprowadzanych przez użytkowników).
* **Architektura REST API:** Wyraźny podział logiki na interfejs sieciowy (`main.py`), operacje bazodanowe (`crud_operations.py`) i agregację danych analitycznych (`reports.py`).

---

## 🛠 Instrukcja uruchomienia

1. **Konfiguracja Bazy Danych:**
   * Zaimportuj pliki `schema.sql` oraz `data.sql` do swojego serwera MySQL (np. za pomocą MySQL Workbench).
   * Skonfiguruj parametry połączenia z bazą (host, user, password) w pliku `db_config.py`.
2. **Instalacja zależności Backendowych:**
   * Otwórz terminal w głównym folderze projektu i zainstaluj wymagane pakiety:
     ```bash
     pip install flask flask-cors pymysql
     ```
3. **Uruchomienie serwera API:**
   * Wystartuj aplikację backendową poleceniem:
     ```bash
     python main.py
     ```
   * Serwer nasłuchuje lokalnie na porcie 5000 (`http://127.0.0.1:5000`).
4. **Uruchomienie Frontendu:**
   * Otwórz plik `index.html` (znajdujący się w folderze frontendu) bezpośrednio w dowolnej przeglądarce internetowej.

---

## 🗄 Schemat Bazy Danych (ERD)

<img width="1154" height="562" alt="image" src="https://github.com/user-attachments/assets/77861853-bae4-4087-ae54-a434add51225" />

### Opis Tabel

#### 1. `Books`
Katalog wszystkich tytułów książkowych w systemie.
* **`id`** (INT, PK): Unikalny identyfikator tytułu.
* **`title`** (VARCHAR): Tytuł książki.
* **`author`** (VARCHAR): Imię i nazwisko autora.
* **`genre`** (VARCHAR): Gatunek literacki.
* **`publisher`** (VARCHAR): Wydawnictwo.
* **`release_date`** (DATETIME): Data wydania.
* **`price`** (DECIMAL 10,2): Standardowa cena katalogowa za nową sztukę.

#### 2. `Storage`
Fizyczny magazyn zarządzający stanem poszczególnych egzemplarzy.
* **`id`** (INT, PK): Unikalny identyfikator wpisu magazynowego.
* **`book_id`** (INT, FK): Klucz obcy łączący z tabelą `Books`.
* **`condition`** (VARCHAR): Stan fizyczny egzemplarza ("new", "used", "damaged").
* **`in_stock`** (INT): Ilość sztuk dostępnych aktualnie w magazynie.
* **`discount`** (DECIMAL 10,2): Przypisany rabat kwotowy (głównie dla outletu).

#### 3. `Customers`
Dane osobowe i kontaktowe zarejestrowanych klientów.
* **`id`** (INT, PK): Unikalny identyfikator klienta.
* **`first_name`** (VARCHAR): Imię klienta.
* **`last_name`** (VARCHAR): Nazwisko klienta.
* **`address`** (VARCHAR): Adres dostawy.
* **`phone`** (VARCHAR): Numer telefonu kontaktowego.
* **`email`** (VARCHAR): Adres e-mail.

#### 4. `Orders`
Główne informacje o zrealizowanych transakcjach.
* **`id`** (INT, PK): Unikalny numer zamówienia.
* **`customer_id`** (INT, FK): Klucz obcy łączący z klientem (`Customers`).
* **`order_date`** (DATETIME): Dokładna data i czas złożenia zamówienia.
* **`total_amount`** (DECIMAL 10,2): Łączna kwota do zapłaty za całe zamówienie.

#### 5. `Order_Details`
Tabela łącząca (wiele-do-wielu) zamówienia z konkretnymi pozycjami na magazynie.
* **`order_id`** (INT, FK): Klucz obcy zamówienia (`Orders`).
* **`storage_id`** (INT, FK): Klucz obcy konkretnej pozycji z magazynu (`Storage`).
* **`quantity`** (INT): Ilość zakupionych sztuk danego produktu.
* **`price`** (DECIMAL 10,2): Cena jednostkowa produktu w momencie zakupu (zabezpieczenie historyczne na wypadek zmiany cen w przyszłości).

---

## 🔗 Relacje w systemie
* **Books 1:N Storage**: Jeden tytuł z katalogu może mieć wiele wpisów w magazynie (np. jedna pula to nowe egzemplarze, inna pula to egzemplarze ze zwrotów z nałożonym rabatem).
* **Customers 1:N Orders**: Jeden zarejestrowany klient może wygenerować wiele niezależnych zamówień w czasie.
* **Orders 1:N Order_Details**: Jedno zamówienie (`Koszyk`) może składać się z wielu różnych pozycji magazynowych.
* **Storage 1:N Order_Details**: Przedmioty z magazynu są ściśle powiązane z historią zamówień, aby zachować ciągłość danych sprzedażowych.

---

###  Warstwa wizualna
Interfejs stworzony w **HTML** wspieranym przez skrypty **JavaScript**. Do uzyskania estetycznego wyglądu oraz wyświetlania ikon wykorzystany został framework **Bootstrap**.


**Co zawiera frontend:**
+ **Strona główna**
    - możliwość wysuzkiwania ksiązek po autorze/ tytule
    - podsumowanie, dostępnych tytułów, ilość książek w putlecie i ile jest zamówień
    - sekcja top 3 najczęściej zamawianych książek z odnośnikiem do danej książki
+ **Sekcje wyświetlania książek**
    Podstrony na których możemy wyświetlić wszystkie książki lub z konkretnej kategorii
+ **Profil**
    Przykładowy widok profilu zalogowanego użytkownika (Klient nr 1), umożliwiający:
     - zobaczenia danych klienta
     - zmienić jakieś dane
     - zobaczyć historię zamówień klienta
+ **Panel admina** (podzielony na cztery kafelki)
    - Stany magazynu: widzimy jakie ksiązki mamy w jakim stanie i ile kosztują, można usunąć jakąś z magazynu
    - Dodaj książkę: formularz dzięki któremy możemy dodać jakąś książkę do bazy
    - Zarejestruj klienta: folmularz dzięki któremy możemy dodać klienta do bazy
    - Raporty i analizy: możliwość wyświetlenia przychodów, lojalnych klientów i braków magazynowych
  
---

### Warstwa serwerowa

Część serwerowa została napisana przy użyciu frameworka **Flask**

**Jak działa `main.py`:**

1. Na starcie Flask uruchamia lokalny serwer na komputerze (`port 5000`)
2. W pliku zdefiniowane są dedykowane endpointy podzielone na sekcje dla klienta, admina oraz książek
3. W momencie, gdy JavaScript wywoła funkcję `fetch()`, serwer przechwytuje zapytanie i uruchamia funkcję przypisaną do danego endpointu
4. Funkcje te przetwarzają dane wejściowe i wykorzystują wcześniej napisane, funkcje SQL do komunikacji z bazą, zwracając wyniki z powrotem na frontend

---
## CRUD

### CREATE

`register_client(imie, nazwisko, adres, telefon, email)` - Rejestruje nowego klienta w bazie danych, Zwraca ID nowo utworzonego klienta

`create_book(tytul, autor, gatunek, wydawnictwo, data_wydania, cena)` -     Dodaje nową książkę do ogólnego katalogu (tabela Books), Zwraca ID nowo dodanej książki

`add_book_to_storage(id_ksiazki, stan_produktu, ilosc, rabat)` -     Przypisuje książkę z katalogu do fizycznego magazynu (tabela Storage) z określeniem jej stanu (new/used/damaged) ilości oraz ewentualnego rabatu


### READ

`get_outlet_books(condition)` -  Pobiera listę książek z kategorii outlet na podstawie podanego stanu

`get_regular_books()` - Pobiera listę nowych książek

`get_all_books()` - Pobiera wszystkie książki

`get_customer_by_name(first_name, last_name)` - Wyświetla podstawowe dane klienta

`search_books(cond)` - Wyświetla książki o danym tytule lub danego autora

`get_customer_order_history(customer_id)` - Pobiera pełną historię zamówień dla jednego konkretnego klienta na podstawie jego ID

### UPDATE

`update_customer_contact(customer_id, field_name, new_value)` - Zmienia jedno wybrane pole tekstowe klienta np. imię czy nazwisko

`restock_storage(storage_id, quantity_to_add)` - Obsługuje dostawę towaru - zwiększa liczbę sztuk w magazynie o podaną wartość

`decrease_storage_stock(storage_id, quantity_to_remove)` - Obsługuje zakup książki - zmniejsza stan magazynowy pod warunkiem że jest wystarczająca ilość, Zwraca True jeśli się udało, lub False jeśli brakło towaru

`update_storage_discount(storage_id, new_discount)` -  Zmienia lub nakłada nową wartość rabatu dla danej pozycji w magazynie

`move_book_to_outlet(storage_id, new_condition, discount=0)` - Zmienia status książki i nakłada ewentualną promocję


### DELETE

`delete_storage_item(storage_id)` - Usuwa książkę z magazynu ale tylko wtedy gdy nikt jej jeszcze nie zamówił, Operacja się nie powiedzie jeśli książka była kiedyś zamawiana

`cancel_order(order_id)` - Anuluje całe zamówienie, Najpierw usuwa rekordy z tabeli Order_Details a następnie usuwa główne zamówienie z tabeli Orders

`delete_customer(customer_id)` - Usuwa konto klienta z bazy danych, Operacja się nie powiedzie jeśli klient posiada już jakąś historię zamówień

---

## Raporty

---

## Transakcja
