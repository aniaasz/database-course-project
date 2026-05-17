# Mini-project 📂


## 🫂 Authors:
Marta Komar, Anna Sznajder

## 📜 Description
A bookstore where users can purchase books in two categories:
* **Regular:** Brand-new books at standard prices.
* **Outlet:** Slightly damaged or pre-owned books at a discount.

## 💻 Technologies
Python + MySQL

---

## Schema

<img width="1154" height="562" alt="image" src="https://github.com/user-attachments/assets/77861853-bae4-4087-ae54-a434add51225" />



## Tables Description

### 1. `Books`
Stores the catalog of all book titles.
* **`id`** (INT, PK): Unique identifier for each book title.
* **`title`** (VARCHAR): The title of the book.
* **`author`** (VARCHAR): The author's name.
* **`genre`** (VARCHAR): The genre of the book.
* **`publisher`** (VARCHAR): The publishing house.
* **`release_date`** (DATETIME): The official publication date.
* **`price`** (DECIMAL 10,2): The standard price for a new copy.

### 2. `Storage`
Manages physical stock and item conditions.
* **`id`** (INT, PK): Unique identifier for the stock entry.
* **`book_id`** (INT, FK): Reference to the `Books` table.
* **`condition`** (VARCHAR): Current state of the book ("New", "Used", "Damaged").
* **`in_stock`** (INT): The quantity currently available in the warehouse.
* **`discount`** (DECIMAL 10,2): Specific price reduction.

### 3. `Customers`
Stores personal details of registered users.
* **`id`** (INT, PK): Unique identifier for the customer.
* **`first_name`** (VARCHAR): Customer's first name.
* **`last_name`** (VARCHAR): Customer's last name.
* **`address`** (VARCHAR): Shipping address.
* **`phone`** (VARCHAR): Contact phone number.
* **`email`** (VARCHAR): Customer's email address.

### 4. `Orders`
Records the main information about every transaction.
* **`id`** (INT, PK): Unique order number.
* **`customer_id`** (INT, FK): Reference to the `Customers` table.
* **`order_date`** (DATETIME): The date and time when the order was placed.
* **`total_amount`** (DECIMAL 10,2): The total calculated price for the entire order.

### 5. `Order Details`
A table that links orders to specific products in the storage.
* **`order_id`** (INT, FK): Reference to the `Orders` table.
* **`storage_id`** (INT, FK): Reference to the specific stock item from `Storage`.
* **`quantity`** (INT): Number of units purchased.
* **`price`** (DECIMAL 10,2): The unit price at the time of purchase (historical data preservation).

---

## Relationships
* **Books 1:N Storage**: A title can have multiple stock types (e.g., one row for brand new copies, another for outlet copies with a discount).
* **Customers 1:N Orders**: A single customer can place many orders over time.
* **Orders 1:N Order Details**: One order can consist of multiple different items.
* **Storage 1:N Order Details**: Items from storage are linked to order details to track exactly what condition of the book was sold.
