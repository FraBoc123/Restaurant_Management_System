import mysql.connector
from getpass import getpass

def create_connection(username = "root", password = "fbciao12321"):
    connection = mysql.connector.connect(
        host="localhost",
        user=username,
        password=password,
        database="resturantManagement",
        auth_plugin="mysql_native_password"
    )
    return connection


def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")

def login():
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")

    connection = None
    user_role = None

    # Connect to the database using the application's MySQL user
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Check if the username is one of the pre-set logins
        if username in ["owner_admin", "manager", "staff"]:
            user_role = username
        else:
            query = """
                SELECT role FROM employee WHERE username = %s AND password = %s;
            """

            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                user_role = result[0]
            else:
                print("Invalid username or password.")
                return None, None

    except mysql.connector.Error as error:
        print("Error connecting to the database.")
        return None, None

    return connection, user_role, username

# def login():
#     username = input("Enter your username: ")
#     password = getpass("Enter your password: ")
#
#     connection = None
#     user_role = None
#
#     try:
#         connection = create_connection(username, password)
#         cursor = connection.cursor()
#
#         # Check if the username is one of the pre-set logins
#         if username in ["owner_admin", "manager", "staff"]:
#             user_role = username
#         else:
#             query = """
#                 SELECT role FROM employee WHERE username = %s;
#             """
#
#             cursor.execute(query, (username,))
#             result = cursor.fetchone()
#
#             if result:
#                 user_role = result[0]
#             else:
#                 print("Invalid username or password.")
#                 return None, None
#
#     except mysql.connector.Error as error:
#         print("Invalid username or password.")
#         return None, None
#
#     return connection, user_role


# DASHBOARD
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
def add_menu_item(connection, restaurant_id):
    name = input("Enter the menu item name: ")
    description = input("Enter the menu item description: ")
    item_type = input("Enter the menu item type: ")
    price = float(input("Enter the menu item price: "))
    resturant_id = restaurant_id

    cursor = connection.cursor()

    query = """
        INSERT INTO menu_items (name, description, item_type, price, resturant_id)
        VALUES (%s, %s, %s, %s, %s);
    """

    cursor.execute(query, (name, description, item_type, price, resturant_id))
    connection.commit()

    print("New menu item added successfully!")

def remove_menu_item(connection): #need to fix (should remove based on restaurant)
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

def display_menu(connection): #need to make for specific restaurant
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
def add_employee(connection, restaurant_id):
    name = input("Enter the employee name: ")
    role = input("Enter the employee role: ")
    username = input("Enter the employee username: ")
    password = input("Enter the employee password: ")
    resturant_id = restaurant_id

    cursor = connection.cursor()

    query = """
        INSERT INTO employee (name, role, username, password, resturant_id)
        VALUES (%s, %s, %s, %s, %s);
    """

    cursor.execute(query, (name, role, username, password, resturant_id))
    connection.commit()

    print("New employee added successfully!")

def remove_employee(connection): # need to write from which restaurant? maybe not
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

def display_employee_list(connection, restaurant_id): #NEED TO MAKE THIS BY RESTAURANT
    cursor = connection.cursor()

    query = """
            SELECT * FROM employee WHERE resturant_id = %s;
        """

    cursor.execute(query, (restaurant_id,))
    employees = cursor.fetchall()

    print("Employee List:")
    for employee in employees:
        print(f"ID: {employee[0]}, Name: {employee[1]}, Role: {employee[2]}, Username: {employee[3]}, Resturant ID: {employee[5]}")

#ORDER MANAGEMENT
def create_new_order(connection): # NEED TO ADD RESTAURANT
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

def add_menu_items_to_order(connection, order_id): # NEED TO Specify Restaurant
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


def update_order_status(connection, order_id): #Add restaurant id
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

#PROMPT USER FOR RESTAURANT BEFORE SHOWING DASHBOARD
# def select_restaurant(connection, username):
#     cursor = connection.cursor()
#
#     query = """
#         SELECT r.* FROM resturant r
#         JOIN employee e ON r.resturant_id = e.resturant_id
#         WHERE e.username = %s;
#     """
#
#     cursor.execute(query, (username,))
#     restaurants = cursor.fetchall()
#
#     if not restaurants:
#         print("No restaurants found.")
#         return None
#
#     print("Available Restaurants:")
#     for restaurant in restaurants:
#         print(f"ID: {restaurant[0]}, Name: {restaurant[1]}")
#
#     while True:
#         restaurant_id = int(input("Enter the ID of the restaurant you want to select: "))
#         selected_restaurant = [restaurant for restaurant in restaurants if restaurant[0] == restaurant_id]
#
#         if selected_restaurant:
#             return selected_restaurant[0][0]
#         else:
#             print("Invalid restaurant ID. Please try again.")
def select_restaurant(connection, username):
    with connection.cursor() as cursor:
        query = f"""
        SELECT r.resturant_id, r.name
        FROM employee re
        JOIN resturant r ON re.resturant_id = r.resturant_id
        WHERE re.username = '{username}'
        """
        cursor.execute(query)
        restaurants = cursor.fetchall()

        if len(restaurants) == 0:
            print("You are not associated with any restaurants.")
            return None

        print("\nPlease select a restaurant:")
        for i, restaurant in enumerate(restaurants):
            print(f"{i + 1}. {restaurant[1]}")  # Change this line

        while True:
            try:
                choice = int(input("Enter the number corresponding to the restaurant: "))
                if 1 <= choice <= len(restaurants):
                    return restaurants[choice - 1][0]  # Change this line
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")



def main():
    connection = None
    user_role = None
    username = None
    while connection is None or user_role is None:
        connection, user_role, username = login()

    #select restaurant
    restaurant_id = None

    while restaurant_id is None:
        restaurant_id = select_restaurant(connection, username)

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

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            add_employee(connection, restaurant_id)
        elif choice == 2:
            display_employee_list(connection, restaurant_id)
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
