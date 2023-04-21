import mysql.connector
from getpass import getpass


# Established Database Connection
def create_connection():

    noError = True

    while noError:
        try:
            username = input("Enter your database username: ")
            password = getpass("Enter your database password: ")

            connection = mysql.connector.connect(
                host="localhost",
                user=username,
                password=password,
                database="resturantManagement",
                auth_plugin="mysql_native_password"
            )

            noError = False
        except mysql.connector.Error as error:
            print("Error connecting to the database.")
            print('Fix Username or Password')
            noError = True

    print("Database Connection Established \n")
    return connection


# Closes Database Connection
def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")


# Login to an employee account
def login(connection):
    user_role = None

    cursor = connection.cursor()

    username = input("Enter your employee username: ")
    password = getpass("Enter your employee password: ")

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

    return user_role, username


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


def display_restaurant_menu(connection, restaurant_id):
    cursor = connection.cursor()

    query = """
        SELECT * FROM menu_items WHERE resturant_id = %s;
    """

    cursor.execute(query, (restaurant_id,))
    menu_items = cursor.fetchall()

    print("Menu:")
    for item in menu_items:
        print(f"ID: {item[0]}, Name: {item[1]}, Description: {item[2]}, Type: {item[3]}, Price: {item[4]}, Restaurant ID: {item[5]}")


def add_menu_item(connection, restaurant_id):
    name = input("Enter the menu item name: ")
    description = input("Enter the menu item description: ")
    item_type = input("Enter the menu item type: ")
    price = input("Enter the menu item price: ")

    cursor = connection.cursor()

    query = """
        CALL add_menu_item(%s, %s, %s, %s, %s);
    """

    try:
        cursor.execute(query, (name, description, item_type, price, restaurant_id))
        connection.commit()
        print("New menu item added successfully!")

    except Exception as e:
        print(f"Error: {e}")


def remove_menu_item(connection):
    menu_item_id = int(input("Enter the menu item ID to remove: "))

    cursor = connection.cursor()

    query = """
        CALL remove_menu_item(%s, @affected_rows);
    """

    try:
        cursor.execute(query, (menu_item_id,))
        cursor.execute("SELECT @affected_rows")
        affected_rows = cursor.fetchone()[0]
        connection.commit()

        if affected_rows > 0:
            print(f"Menu item ID {menu_item_id} removed successfully!")
        else:
            print(f"No menu item found with ID {menu_item_id}")

    except Exception as e:
        print(f"Error: {e}")


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


def add_employee(connection, restaurant_id):
    name = input("Enter the employee name: ")
    role = input("Enter the employee role: ")
    username = input("Enter the employee username: ")
    password = input("Enter the employee password: ")

    cursor = connection.cursor()

    query = """
        CALL add_employee(%s, %s, %s, %s, %s);
    """

    try:
        cursor.execute(query, (name, role, username, password, restaurant_id))
        connection.commit()
        print("New employee added successfully!")

    except Exception as e:
        print(f"Error: {e}")


def remove_employee(connection):
    employee_id = int(input("Enter the employee ID to remove: "))

    cursor = connection.cursor()

    query = """
        CALL remove_employee(%s, @affected_rows);
    """

    try:
        cursor.execute(query, (employee_id,))
        cursor.execute("SELECT @affected_rows")
        affected_rows = cursor.fetchone()[0]
        connection.commit()

        if affected_rows > 0:
            print(f"Employee ID {employee_id} removed successfully!")
        else:
            print(f"No employee found with ID {employee_id}")

    except Exception as e:
        print(f"Error: {e}")


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


def create_new_order(connection, restaurant_id):
    table_num = int(input("Enter the table number: "))
    customer_num = int(input("Enter the number of customers: "))

    cursor = connection.cursor()

    query = """
        CALL create_new_order(%s, %s, %s, @order_id);
    """

    cursor.execute(query, (table_num, customer_num, restaurant_id))
    cursor.execute("SELECT @order_id")
    order_id = cursor.fetchone()[0]
    connection.commit()

    while True:
        menu_item_id = int(input("Enter the dish ID: "))
        quantity = int(input("Enter the quantity: "))

        query = """
            call add_menu_order(%s, %s, %s, @message);
        """

        cursor.execute(query, (menu_item_id, order_id, quantity))
        connection.commit()

        more_dishes = input("Do you want to add more dishes? (yes/no): ")
        if more_dishes.lower() != 'yes':
            break

    return order_id


def add_menu_items_to_order(connection, order_id): #showing example of how to show sql error (for the rest of the functions we used python for error handling)
    while True:
        menu_item_id = int(input("Enter the menu item ID to add (0 to stop): "))
        if menu_item_id == 0:
            break

        amount = int(input("Enter the amount of the menu item: "))

        cursor = connection.cursor()

        query = """
            call add_menu_order(%s, %s, %s, @message);
        """

        try:
            cursor.execute(query, (menu_item_id, order_id, amount))
            cursor.execute("SELECT @message")
            message = cursor.fetchone()[0]
            connection.commit()
            print(message)

        except Exception as e:
            print(f"Error: {e}")


def update_order_status(connection, order_id):
    incorrectStatus = True

    while incorrectStatus:
        new_status = input("Enter the new order status (In Progress, Complete): ")
        incorrectStatus = not (new_status.lower() == "in progress" or new_status.lower() == "complete")

    cursor = connection.cursor()

    query = """
        CALL update_order_status(%s, %s);
    """

    try:
        cursor.execute(query, (order_id, new_status))
        connection.commit()
        print(f"Order ID {order_id} status updated to {new_status}")

    except Exception as e:
        print(f"Error: {e}")


def calculate_bill(connection, order_id):
    try:
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
    except:
        print("error")


def select_restaurant(connection, username):
    cursor = connection.cursor()

    query = """
        CALL select_restaurant(%s, @resturant_id, @resturant_name);
    """

    cursor.execute(query, (username,))
    cursor.execute("SELECT @resturant_id, @resturant_name")
    restaurant = cursor.fetchone()

    if not restaurant or restaurant[0] is None:
        print("You are not associated with any restaurants.")
        return None

    resturant_id, resturant_name = restaurant
    print(f"Selected restaurant: {resturant_name}")
    return resturant_id


def main():
    try:
        connection = create_connection()
        user_role = None
        username = None
        while connection is None or user_role is None:
            user_role, username = login(connection)

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
            print("6. Display Restaurant Menu")
            print("7. Create New Order")
            print("8. Add Menu Items to Order")
            print("9. Update Order Status")
            print("10. Calculate Bill")
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
                add_menu_item(connection, restaurant_id)
            elif choice == 5:
                remove_menu_item(connection)
            elif choice == 6:
                display_restaurant_menu(connection, restaurant_id)
            elif choice == 7:
                order_id = create_new_order(connection, restaurant_id)
            elif choice == 8:
                if 'order_id' in locals():
                    add_menu_items_to_order(connection, order_id)
                else:
                    print("Create a new order first.")
            elif choice == 9:
                if 'order_id' in locals():
                    update_order_status(connection, order_id)
                else:
                    print("Create a new order first.")
            elif choice == 10:
                if 'order_id' in locals():
                    calculate_bill(connection, order_id)
                else:
                    print("Create a new order first.")
            elif choice == 0:
                connection.close()
                break
            else:
                print("Invalid choice. Please try again.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()


#need to be asked which order you refer to when making orders. for now its only one at a time
#Automatically make order in progress once order is created