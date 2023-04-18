drop database if exists `resturantManagement`;
CREATE DATABASE resturantManagement;

USE resturantManagement;

drop table if exists `resturant`;
CREATE TABLE resturant 
(
	resturant_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(150) NOT NULL,
    description VARCHAR(500) NOT NULL
);
drop table if exists `employee`;

-- updated pk constraints
CREATE TABLE employee
(
	employee_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    resturant_id INT,
    FOREIGN KEY (resturant_id) REFERENCES resturant(resturant_id) ON UPDATE CASCADE ON DELETE CASCADE
);


drop table if exists `shifts`;
CREATE TABLE shifts
(
	shift_id INT PRIMARY KEY,
    job_type VARCHAR(100) NOT NULL,
    time TIME NOT NULL,
    date DATE NOT NULL
);

drop table if exists `menu_items`;
CREATE TABLE menu_items
(
	menu_item_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(500) NOT NULL,
    item_type VARCHAR(100) NOT NULL,
    price DOUBLE NOT NULL,
	resturant_id INT,
    FOREIGN KEY (resturant_id) REFERENCES resturant(resturant_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- added auto increment
drop table if exists `customer_group`;
CREATE TABLE customer_group     -- NEED TO ADD RESTAURANT ID - MAYBE EACH RESTAURANT HAS TABLES AND SEATING FOR EACH TABLE 
(
	customer_group_id INT AUTO_INCREMENT PRIMARY KEY,
    table_num INT NOT NULL,
    customer_num INT NOT NULL,
    resturant_id INT NOT NULL,
    FOREIGN KEY (resturant_id) REFERENCES resturant(resturant_id) ON UPDATE CASCADE ON DELETE CASCADE
);

drop table if exists `orders`;
CREATE TABLE orders
(
	order_id INT AUTO_INCREMENT PRIMARY KEY,
    status ENUM('In Progress', 'Complete'),
    customer_group_id INT,
    FOREIGN KEY (customer_group_id) REFERENCES customer_group(customer_group_id) ON UPDATE CASCADE ON DELETE CASCADE
);

drop table if exists `ingredients`;
CREATE TABLE ingredients
(
	ingredient_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    supply_amount INT NOT NULL,
    price DOUBLE NOT NULL
);

drop table if exists `employee_shift`;
CREATE TABLE employee_shift
(
	employee_id INT,
    shift_id INT,
    PRIMARY KEY (employee_id, shift_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (shift_id) REFERENCES shifts(shift_id) ON UPDATE CASCADE ON DELETE CASCADE
);

drop table if exists `menu_order`;
CREATE TABLE menu_order
(
	menu_item_id INT,
    order_id INT,
    amount INT NOT NULL,
    PRIMARY KEY (menu_item_id, order_id),
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(menu_item_id) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (order_id) REFERENCES orders(order_id) ON UPDATE CASCADE ON DELETE CASCADE
);

drop table if exists `menu_ingredients`;
CREATE TABLE menu_ingredients
(
	menu_item_id INT,
    ingredient_id INT,
    PRIMARY KEY (menu_item_id, ingredient_id),
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(menu_item_id) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id) ON UPDATE CASCADE ON DELETE CASCADE
);


-- create procedures
drop procedure if exists add_menu_order;

delimiter $$
create procedure add_menu_order(menu_item_id_p INT, order_id_p INT, amount_p INT)
	begin
        if (select exists(select * from menu_items where menu_items.menu_item_id = menu_item_id_p)) then
			INSERT INTO menu_order (menu_item_id, order_id, amount)
            VALUES (menu_item_id_p, order_id_p, amount_p)
            ON DUPLICATE KEY UPDATE amount = amount + amount_p;
		else
			select 'Menu Item Not Available';
			signal sqlstate '42000' set message_text = 'Menu Item not found';
		end if;
    end $$
delimiter ;

drop procedure if exists get_order_details;

delimiter $$
create procedure get_order_details(order_id_p INT)
	begin
        SELECT menu_items.menu_item_id, menu_items.name, menu_items.price, menu_order.amount
        FROM menu_items
        INNER JOIN menu_order ON menu_items.menu_item_id = menu_order.menu_item_id
        WHERE menu_order.order_id = order_id_p;
    end $$
delimiter ;



-- inserting values into tables
INSERT INTO resturant (resturant_id, name, address, description)
VALUES (1, 'La Trattoria', '123 Main St', 'Italian cuisine at its finest'),
       (2, 'Le Bistro', '456 Elm St', 'French-inspired dishes in a cozy atmosphere'),
       (3, 'El Taquito', '789 Maple Ave', 'Authentic Mexican food made with fresh ingredients');

INSERT INTO employee (employee_id, name, role, username, password, resturant_id)
VALUES (1, 'John Smith', 'Manager', 'jsmith', 'password', 1),
       (2, 'Jane Doe', 'Chef', 'jdoe', 'password', 1),
       (3, 'Bob Johnson', 'Waiter', 'bjohnson', 'password', 1),
       (4, 'Alice Lee', 'Manager', 'alee', 'password', 2),
       (5, 'Tom Wilson', 'Chef', 'twilson', 'password', 2),
       (6, 'Emily Chen', 'Waiter', 'echen', 'password', 2),
       (7, 'Mike Brown', 'Manager', 'mbrown', 'password', 3),
       (8, 'Lisa Kim', 'Chef', 'lkim', 'password', 3),
       (9, 'David Rodriguez', 'Waiter', 'drodriguez', 'password', 3);

INSERT INTO shifts (shift_id, job_type, time, date)
VALUES (1, 'Manager', '10:00:00', '2023-04-06'),
       (2, 'Chef', '12:00:00', '2023-04-06'),
       (3, 'Waiter', '14:00:00', '2023-04-06'),
       (4, 'Manager', '16:00:00', '2023-04-06'),
       (5, 'Chef', '18:00:00', '2023-04-06'),
       (6, 'Waiter', '20:00:00', '2023-04-06');


INSERT INTO menu_items (menu_item_id, name, description, item_type, price, resturant_id)
VALUES
  (1, 'Spaghetti Bolognese', 'Classic Italian spaghetti with tomato sauce and ground beef', 'Main', 12.99, 1),
  (2, 'Margherita Pizza', 'Classic Italian pizza with tomato sauce, mozzarella, and basil', 'Main', 9.99, 1),
  (3, 'Caesar Salad', 'Romaine lettuce, croutons, Parmesan cheese, and Caesar dressing', 'Appetizer', 6.99, 1),
  (4, 'Garlic Bread', 'Toasted bread with garlic butter and Parmesan cheese', 'Appetizer', 4.99, 1),
  (5, 'Tiramisu', 'Classic Italian dessert with ladyfingers, espresso, mascarpone cheese, and cocoa', 'Dessert', 7.99, 1);


INSERT INTO customer_group (customer_group_id, table_num, customer_num, resturant_id) 
VALUES   
  (1, 1, 2, 1),   
  (2, 2, 4, 1),   
  (3, 3, 6, 2);



INSERT INTO orders (order_id, status, customer_group_id)
VALUES
  (1, 'In Progress', 1),
  (2, 'In Progress', 2),
  (3, 'Complete', 3);


INSERT INTO ingredients (ingredient_id, name, supply_amount, price)
VALUES
  (1, 'Ground Beef', 100, 4.99),
  (2, 'Spaghetti', 50, 2.99),
  (3, 'Tomato Sauce', 200, 1.99),
  (4, 'Mozzarella Cheese', 100, 3.99),
  (5, 'Bread', 50, 1.99),
  (6, 'Garlic', 20, 0.99);


INSERT INTO employee_shift (employee_id, shift_id)
VALUES
  (1, 1),
  (2, 2),
  (3, 3),
  (4, 1),
  (5, 2),
  (6, 3);


INSERT INTO menu_order (menu_item_id, order_id, amount)
VALUES
  (1, 1, 2),
  (2, 1, 1),
  (3, 2, 4),
  (4, 2, 2),
  (5, 3, 6);


INSERT INTO menu_ingredients (menu_item_id, ingredient_id)
VALUES
  (1, 1),
  (1, 2),
  (1, 3),
  (2, 3),
  (2, 4),
  (4, 5),
  (4, 6);







-- Owner/Admin

drop user if exists 'owner_admin'@'localhost';
CREATE USER 'owner_admin'@'localhost' IDENTIFIED BY 'owner_password';
GRANT ALL PRIVILEGES ON resturantManagement.* TO 'owner_admin'@'localhost';

-- Manager

drop user if exists 'manager'@'localhost';
CREATE USER 'manager'@'localhost' IDENTIFIED BY 'manager_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON resturantManagement.* TO 'manager'@'localhost';

-- Chef
drop user if exists 'chef'@'localhost';
CREATE USER 'chef'@'localhost' IDENTIFIED BY 'chef';
GRANT SELECT, INSERT, UPDATE, DELETE ON resturantManagement.menu_items TO 'chef'@'localhost';

-- Server
drop user if exists 'waiter'@'localhost';
CREATE USER 'waiter'@'localhost' IDENTIFIED BY 'waiter';
GRANT SELECT, INSERT ON resturantManagement.orders TO 'waiter'@'localhost';

-- Apply the changes
FLUSH PRIVILEGES;










SELECT PLUGIN_NAME FROM INFORMATION_SCHEMA.PLUGINS WHERE PLUGIN_NAME LIKE 'caching_sha2_password';



SHOW GRANTS FOR 'owner_admin'@'localhost';
ALTER USER 'owner_admin'@'localhost' IDENTIFIED BY 'owner_password';
ALTER USER 'manager'@'localhost' IDENTIFIED BY 'manager_password';
ALTER USER 'waiter'@'localhost' IDENTIFIED BY 'waiter_password';
ALTER USER 'chef'@'localhost' IDENTIFIED BY 'chef_password';


