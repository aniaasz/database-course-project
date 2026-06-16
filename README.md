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
Frontend: HTML, JavaScript, CSS

## 🚀 Funkcjonalności

### Dla Klienta:
* **Przeglądanie katalogu:** Podział asortymentu na książki nowe oraz outletowe (używane, zniszczone).
* **Dynamiczna wyszukiwarka:** Możliwość szybkiego wyszukiwania książek po tytule lub autorze.
* **Profil Użytkownika:** Podgląd profilu klienta z dynamicznym formularzem umożliwiającym edycję danych kontaktowych.
* **Historia Zamówień:** Szczegółowy wykaz zrealizowanych zakupów z automatycznie przeliczanymi kwotami i tłumaczeniem stanów fizycznych książek.

### Dla Administratora (Panel Admina):
* **Zarządzanie asortymentem (CRUD):** Dodawanie nowych tytułów do bazy oraz przypisywanie ich do fizycznego magazynu, wraz z bezpiecznym usuwaniem asortymentu.
* **Rejestracja klientów:** Dodawanie nowych użytkowników do systemu.
* **System Raportowy:** * Analiza przychodów wg stanu książek.
  * Raport lojalnościowy (TOP 5 klientów z największą sumą zamówień).
  * Alert krytycznych stanów magazynowych (wyszukiwanie braków asortymentu).

---

## ⚙️ Zaawansowane mechaniki bazodanowe i architektoniczne
Projekt został zbudowany z zachowaniem profesjonalnych praktyk inżynieryjnych:
* **Transakcje i reguły ACID:** Zastosowanie mechanizmów blokowania (`FOR UPDATE`) oraz kontroli transakcji (`connection.rollback()` i `commit()`) w celu zapobiegania "race conditions" podczas modyfikacji danych.
* **Idempotentność skryptów:** Użycie klauzuli `ON DUPLICATE KEY UPDATE` w pliku testowym `data.sql`, co zapewnia odporność bazy na błędy przy wielokrotnym ładowaniu tych samych danych.
* **Ochrona przed SQL Injection:** Pełna parametryzacja zapytań bazodanowych (wykorzystanie `%s` przy przekazywaniu danych wprowadzanych przez użytkowników).
* **Architektura REST API:** Wyraźny podział logiki na interfejs sieciowy (`app.py`), operacje bazodanowe (`crud_operations.py`) i agregację danych analitycznych (`reports.py`).

---

## 🛠 Instrukcja uruchomienia (How to run)

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
     python app.py
     ```
   * Serwer nasłuchuje lokalnie na porcie 5000 (`http://127.0.0.1:5000`).
4. **Uruchomienie Frontendu:**
   * Otwórz plik `index.html` (znajdujący się w folderze frontendu) bezpośrednio w dowolnej nowoczesnej przeglądarce internetowej.

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

