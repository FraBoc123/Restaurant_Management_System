import mysql.connector
from mysql.connector import Error
from getpass import getpass


def create_connection(username, password):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=username,
            password=password,
            database="resturantManagement"
        )

        if connection.is_connected():
            print("Connected to MySQL Server")
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None


def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")

def login():
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")

    connection = create_connection(username, password)
    if connection:
        return connection
    else:
        print("Invalid username or password.")
        return None

#DASHBOARD
def dashboard(connection):
    cursor = connection.cursor()

    query = """
        SELECT COUNT(*) FROM orders
        WHERE status = 'In Progress';
    """

    cursor.execute(query)
    orders_in_progress = cursor.fetchone()[0]

    print("Dashboard:")
    print(f"Orders in progress: {orders_in_progress}")


# Add your dashboard logic here
#

#MENU MANAGEMENT
def add_menu_item(connection):
    name = input("Enter the menu item name: ")
    description = input("Enter the menu item description: ")
    item_type = input("Enter the menu item type: ")
    price = float(input("Enter the menu item price: "))
    restaurant_id = int(input("Enter the restaurant ID: "))

    cursor = connection.cursor()

    query = """
        INSERT INTO menu_items (name, description, item_type, price, restaurant_id)
        VALUES (%s, %s, %s, %s, %s);
    """

    cursor.execute(query, (name, description, item_type, price, restaurant_id))
    connection.commit()

    print("New menu item added successfully!")

def remove_menu_item(connection):
    menu_item_id = int(input("Enter the menu item ID to remove: "))

    cursor = connection.cursor()

    query = """
        DELETE FROM menu_items
        WHERE menu_item_id = %s;
    """

    cursor.execute(query, (menu_item_id,))
    connection.commit()

    if cursor.rowcount > 0:
        print(f"Menu item ID {menu_item_id} removed successfully!")
    else:
        print(f"No menu item found with ID {menu_item_id}")

def display_menu(connection):
    cursor = connection.cursor()

    query = """
        SELECT * FROM menu_items;
    """

    cursor.execute(query)
    menu_items = cursor.fetchall()

    print("Menu:")
    for item in menu_items:
        print(f"ID: {item[0]}, Name: {item[1]}, Description: {item[2]}, Type: {item[3]}, Price: {item[4]}, Restaurant ID: {item[5]}")

#EMPLOYEE MANAGEMENT
def add_employee(connection):
    name = input("Enter the employee name: ")
    role = input("Enter the employee role: ")
    username = input("Enter the employee username: ")
    password = input("Enter the employee password: ")
    restaurant_id = int(input("Enter the restaurant ID: "))

    cursor = connection.cursor()

    query = """
        INSERT INTO employee (name, role, username, password, restaurant_id)
        VALUES (%s, %s, %s, %s, %s);
    """

    cursor.execute(query, (name, role, username, password, restaurant_id))
    connection.commit()

    print("New employee added successfully!")

def remove_employee(connection):
    employee_id = int(input("Enter the employee ID to remove: "))

    cursor = connection.cursor()

    query = """
        DELETE FROM employee
        WHERE employee_id = %s;
    """

    cursor.execute(query, (employee_id,))
    connection.commit()

    if cursor.rowcount > 0:
        print(f"Employee ID {employee_id} removed successfully!")
    else:
        print(f"No employee found with ID {employee_id}")

def display_employee_list(connection):
    cursor = connection.cursor()

    query = """
        SELECT * FROM employee;
    """

    cursor.execute(query)
    employees = cursor.fetchall()

    print("Employee List:")
    for employee in employees:
        print(f"ID: {employee[0]}, Name: {employee[1]}, Role: {employee[2]}, Username: {employee[3]}, Restaurant ID: {employee[5]}")

#ORDER MANAGEMENT
def create_new_order(connection):
    table_num = int(input("Enter the table number: "))
    customer_num = int(input("Enter the number of customers: "))

    cursor = connection.cursor()

    query = """
        INSERT INTO customer_group (table_num, customer_num)
        VALUES (%s, %s);
    """

    cursor.execute(query, (table_num, customer_num))
    connection.commit()
    customer_group_id = cursor.lastrowid

    query = """
        INSERT INTO orders (status, customer_group_id)
        VALUES ('In Progress', %s);
    """

    cursor.execute(query, (customer_group_id,))
    connection.commit()
    order_id = cursor.lastrowid

    print(f"New order created with Order ID: {order_id}")
    return order_id

def add_menu_items_to_order(connection, order_id):
    while True:
        menu_item_id = int(input("Enter the menu item ID to add (0 to stop): "))
        if menu_item_id == 0:
            break

        amount = int(input("Enter the amount of the menu item: "))

        cursor = connection.cursor()

        query = """
            INSERT INTO menu_order (menu_item_id, order_id, amount)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE amount = amount + %s;
        """

        cursor.execute(query, (menu_item_id, order_id, amount, amount))
        connection.commit()

        print(f"Added {amount} of menu item ID {menu_item_id} to Order ID {order_id}")


def update_order_status(connection, order_id):
    new_status = input("Enter the new order status (In Progress, Complete): ")

    cursor = connection.cursor()

    query = """
        UPDATE orders
        SET status = %s
        WHERE order_id = %s;
    """

    cursor.execute(query, (new_status, order_id))
    connection.commit()

    print(f"Order ID {order_id} status updated to {new_status}")

def calculate_bill(connection, order_id):
    cursor = connection.cursor()

    query = """
        SELECT menu_items.menu_item_id, menu_items.name, menu_items.price, menu_order.amount
        FROM menu_items
        INNER JOIN menu_order ON menu_items.menu_item_id = menu_order.menu_item_id
        WHERE menu_order.order_id = %s;
    """

    cursor.execute(query, (order_id,))
    order_items = cursor.fetchall()

    if not order_items:
        print(f"No order found with Order ID {order_id}")
        return

    total_price = 0

    print(f"Bill for Order ID {order_id}:")
    for item in order_items:
        item_id, name, price, amount = item
        item_total_price = price * amount
        total_price += item_total_price
        print(f"Menu Item ID: {item_id}, Name: {name}, Price: {price}, Amount: {amount}, Total Price: {item_total_price}")

    print(f"Total Bill: {total_price}")


def main():
    connection = mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="fbciao12321",
        database="restaurantManagement"
    )

    while True:
        print("\nChoose an option:")
        print("1. Add Employee")
        print("2. Display Employee List")
        print("3. Remove Employee")
        print("4. Add Menu Item")
        print("5. Remove Menu Item")
        print("6. Create New Order")
        print("7. Add Menu Items to Order")
        print("8. Update Order Status")
        print("9. Calculate Bill")
        print("0. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            add_employee(connection)
        elif choice == 2:
            display_employee_list(connection)
        elif choice == 3:
            remove_employee(connection)
        elif choice == 4:
            add_menu_item(connection)
        elif choice == 5:
            remove_menu_item(connection)
        elif choice == 6:
            order_id = create_new_order(connection)
        elif choice == 7:
            if 'order_id' in locals():
                add_menu_items_to_order(connection, order_id)
            else:
                print("Create a new order first.")
        elif choice == 8:
            if 'order_id' in locals():
                update_order_status(connection, order_id)
            else:
                print("Create a new order first.")
        elif choice == 9:
            if 'order_id' in locals():
                calculate_bill(connection, order_id)
            else:
                print("Create a new order first.")
        elif choice == 0:
            break
        else:
            print("Invalid choice. Please try again.")

    connection.close()

if __name__ == "__main__":
    main()
