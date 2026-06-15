INSERT INTO Customers (id, first_name, last_name, address, phone, email)
VALUES (1, 'Adam', 'Nowak', 'Czarnowiejska, 31-025 Kraków', '+48222111333', 'adamnowak@gmail.com')
ON DUPLICATE KEY UPDATE id=id;

USE defaultdb;

INSERT INTO Books (id, title, author, genre, publisher, release_date, price)
VALUES (1, 'Jasna noc', 'Choi Eunyoung', 'powieść obyczajowa', 'Tajfuny', '2026-01-30', 45.00)
    ON DUPLICATE KEY UPDATE id=id;


INSERT INTO Storage (id, book_id, `condition`, in_stock, discount)
VALUES (1, 1, 'new', 10, 0.00)
    ON DUPLICATE KEY UPDATE id=id;

INSERT INTO Orders (id, customer_id, order_date,total_amount)
VALUES (1, 1, '2026-06-13 15:30:00',90.00);

INSERT INTO Order_Details (order_id, storage_id, quantity, price)
VALUES (1, 1, 2, 45.00);

INSERT INTO Books (id, title, author, genre, publisher, release_date, price)
VALUES (5, 'Atomowe nawyki', 'James Clear', 'Poradnik', 'Galaktyka', '2019-11-05', 44.99)
ON DUPLICATE KEY UPDATE id=id;

INSERT INTO Storage (id, book_id, `condition`, in_stock, discount)
VALUES (5, 5, 'damaged', 4, 20.00)
ON DUPLICATE KEY UPDATE id=id;

INSERT INTO Books (id, title, author, genre, publisher, release_date, price)
VALUES (6, 'Ślepnąc od świateł', 'Jakub Żulczyk', 'Thriller', 'Świat Książki', '2014-10-22', 49.00)
ON DUPLICATE KEY UPDATE id=id;

INSERT INTO Storage (id, book_id, `condition`, in_stock, discount)
VALUES (6, 6, 'used', 7, 14.00)
ON DUPLICATE KEY UPDATE id=id;