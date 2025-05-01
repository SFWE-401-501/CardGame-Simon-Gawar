import mysql.connector
import logging

# Configure logging
logging.basicConfig(filename="app_errors.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

# Function to connect to the MySQL database
def connect_to_database():
    """Establish a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(
            host="localhost",  # Replace with your MySQL server address
            user="root",  # Replace with your MySQL username
            password="",  # Replace with your MySQL password
            database="app_database"  # Replace with your MySQL database name
        )
        return conn
    except mysql.connector.Error as err:
        logging.error(f"Error connecting to database: {err}")
        print(f"Error detected: {err}")
        return None

# implementing command injection 
# 
def login(username, password):
    try:
        # Connect to the MySQL database
        conn = connect_to_database()
        if not conn:
            return

        cursor = conn.cursor()

        # Query the database for user credentials Password Security:
        # Store passwords in the database as hashed values using bcrypt or another hashing library in production systems.
        # Compare hashed passwords during login
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result and password == result[0]:
            print(f"Login successful! Welcome, {username}.")
        else:
            raise ValueError("Invalid username or password")
    except ValueError as ve:
        logging.error(f"Authentication Error: {ve}")
        print(f"Error detected: {ve}")
    except mysql.connector.Error as err:
        logging.error(f"MySQL Error: {err}")
        print(f"Database Error: {err}")
    except Exception as e:
        logging.error(f"Unexpected Error: {e}")
        print(f"Error detected: {e}")
    finally:
        if conn:
            conn.close()

def card_sort_and_search():
    try:
        # Placeholder for card sort and search functionality
        print("Sorting and searching cards...")
        cards = ["Card 1", "Card 2", "Card 3", "Card 4","Card 5","Card 6"]
        sorted_cards = sorted(cards)
        print("Sorted cards:", sorted_cards)
    except Exception as e:
        logging.error(f"Error during card sort and search: {e}")
        print(f"Error detected: {e}")

# Simulating user input
try:
    input_username = input("Enter your username: ")
    input_password = input("Enter your password: ")
    login(input_username, input_password)

    # When login is successful, proceed to card sort and search functionality
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = %s", (input_username,))
        result = cursor.fetchone()

        if result and input_password == result[0]:
            card_sort_and_search()
        conn.close()
except Exception as ex:
    logging.error(f"Error during user input: {ex}")
    print(f"Error detected: {ex}")
