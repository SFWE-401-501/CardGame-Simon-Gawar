
import mysql.connector
import logging
import bcrypt
from time import time

# Author: Simon Gawar

# Configuration of the logger to handle errors
logging.basicConfig(filename="app_errors.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

# A dictionary to track login attempts per user (DoS protection)
login_attempts = {}  # Track user attempts to apply rate limiting

def connect_to_database():
    """
    Connect to the MySQL database with a connection timeout for DoS protection.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",       # MySQL server hostname
            user="root",            # MySQL username
            password="",            # MySQL password
            database="app_database",# MySQL database name
            connection_timeout=5    # Timeout to prevent connection hanging
        )
        return conn
    except mysql.connector.Error as err:
        logging.error(f"Error connecting to database: {err}")
        print("Error detected: Database connection issue.")
        return None

def is_rate_limited(username):
    """
    Check if a username exceeds rate limits to prevent DoS attacks.
    Allows a maximum of 5 attempts within 60 seconds per user.
    """
    current_time = time()
    if username not in login_attempts:
        login_attempts[username] = [current_time]
        return False
    else:
        # Remove attempts older than 60 seconds
        login_attempts[username] = [t for t in login_attempts[username] if current_time - t < 60]

        # Check the number of attempts in the last 60 seconds
        if len(login_attempts[username]) >= 5:
            return True
        else:
            login_attempts[username].append(current_time)
            return False

def hash_password(password):
    """
    Hash a password using bcrypt.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def login(username, password):
    """
    Authenticate the user with rate limiting, input validation, and hashed password comparison.
    """
    try:
        # Input validation
        if not isinstance(username, str) or not isinstance(password, str):
            raise ValueError("Invalid input type. Username and password must be strings.")
        if len(username) > 20 or len(password) > 20:
            raise ValueError("Input too long. Username and password must be less than 20 characters.")

        # Rate limiting
        if is_rate_limited(username):
            print(f"Rate limit exceeded for user {username}. Please try again later.")
            return username and password

        # Connect to the database
        conn = connect_to_database()
        if not conn:
            return

        cursor = conn.cursor()

        # Query user credentials
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        # Verify password
        if result and bcrypt.checkpw(password.encode(), result[0].encode()):
            print(f"Login successful! Welcome, {username}.")
        else:
            raise ValueError("Invalid username or password.")
    except ValueError as ve:
        logging.error(f"Authentication Error: {ve}")
        print("Error detected: Invalid credentials.")
    except mysql.connector.Error as err:
        logging.error(f"MySQL Error: {err}")
        print("Database Error: Please try again later.")
    except Exception as e:
        logging.error(f"Unexpected Error: {e}")
        print("Error detected: An unexpected error occurred.")
    finally:
        if conn:
            conn.close()

def card_sort_and_search():
    """
    Perform card sorting and searching.
    """
    try:
        cards = ["Card 1", "Card 2", "Card 3", "Card 4", "Card 5", "Card 6"]
        sorted_cards = sorted(cards)
        print("Sorted cards:", sorted_cards)
    except Exception as e:
        logging.error(f"Error during card sort and search: {e}")
        print("Error detected: Card sorting failed.")

# Main script
try:
    input_username = input("Enter your username: ")
    input_password = input("Enter your password: ")

    # Simulate user login
    login(input_username, input_password)

    # Perform card sort and search if login is successful
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = %s", (input_username,))
        result = cursor.fetchone()

        if result and bcrypt.checkpw(input_password.encode(), result[0].encode()):
            card_sort_and_search()

        conn.close()
except Exception as ex:
    logging.error(f"Error during user input: {ex}")
    print("Error detected: An unexpected error occurred.")
