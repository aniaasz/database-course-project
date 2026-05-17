-- Created by Redgate Data Modeler (https://datamodeler.redgate-platform.com)
-- Last modification date: 2026-04-22 19:48:30.818

-- tables
-- Table: Books
CREATE TABLE Books (
                       id int  NOT NULL AUTO_INCREMENT,
                       title varchar(100)  NOT NULL,
                       author varchar(100)  NOT NULL,
                       genre varchar(100)  NOT NULL,
                       publisher varchar(100)  NOT NULL,
                       release_date date  NOT NULL,
                       price decimal(10,2)  NOT NULL,
                       CONSTRAINT Books_pk PRIMARY KEY (id)
);

-- Table: Customers
CREATE TABLE Customers (
                           id int  NOT NULL AUTO_INCREMENT,
                           first_name varchar(50)  NOT NULL,
                           last_name varchar(50)  NOT NULL,
                           address varchar(50)  NOT NULL,
                           phone  varchar(50)  NOT NULL,
                           email varchar(50)  NOT NULL,
                           CONSTRAINT Customers_pk PRIMARY KEY (id)
);

-- Table: Order_Details
CREATE TABLE Order_Details (
                               id int NOT NULL AUTO_INCREMENT,
                               order_id int  NOT NULL,
                               quantity int  NOT NULL,
                               price decimal(10,2)  NOT NULL,
                               storage_id int  NOT NULL,
                               CONSTRAINT Order_Details_pk PRIMARY KEY (id)
);

-- Table: Orders
CREATE TABLE Orders (
                        id int  NOT NULL AUTO_INCREMENT,
                        customer_id int  NOT NULL,
                        order_date datetime  NOT NULL,
                        total_amount decimal(10,2)  NOT NULL,
                        CONSTRAINT Orders_pk PRIMARY KEY (id)
);

-- Table: Storage
CREATE TABLE Storage (
                         id int  NOT NULL AUTO_INCREMENT,
                         book_id int  NOT NULL,
                         `condition` varchar(50)  NOT NULL,
                         in_stock int  NOT NULL,
                         discount decimal(10,2)  NOT NULL DEFAULT 0,
                         CONSTRAINT Storage_pk PRIMARY KEY (id)
);

-- foreign keys
-- Reference: Customers_Orders (table: Orders)
ALTER TABLE Orders ADD CONSTRAINT Customers_Orders FOREIGN KEY Customers_Orders (customer_id)
    REFERENCES Customers (id);

-- Reference: Orders_Order Details (table: Order_Details)
ALTER TABLE Order_Details ADD CONSTRAINT Orders_Order_Details FOREIGN KEY Orders_Order_Details (order_id)
    REFERENCES Orders (id);

-- Reference: Storage_Books (table: Storage)
ALTER TABLE Storage ADD CONSTRAINT Storage_Books FOREIGN KEY Storage_Books (book_id)
    REFERENCES Books (id);

-- Reference: Storage_Order Details (table: Order_Details)
ALTER TABLE Order_Details ADD CONSTRAINT Storage_Order_Details FOREIGN KEY Storage_Order_Details (storage_id)
    REFERENCES Storage (id);

-- End of file.
