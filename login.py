import mysql.connector  # MySQL database connector
import logging  # Error logging module
import bcrypt  # Library for hashing passwords securely
import random  # Random card generation
from time import time  # Time tracking for rate limiting

# Configure the logger to record errors in a file
logging.basicConfig(filename="app_errors.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

# Dictionary to track login attempts per user for rate limiting (DoS protection)
login_attempts = {}

# Define card suits and values for authentication challenge and password salting
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

def connect_to_database():
    """
    Connect to the MySQL database with a timeout to prevent connection hanging.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",  # MySQL server hostname
            user="root",  # MySQL username
            password="",  # MySQL password (should be securely stored)
            database="app_database",  # MySQL database name
            connection_timeout=5  # Limits connection timeout to 5 seconds
        )
        return conn
    
    
    except mysql.connector.Error as err:
        logging.error(f"Error connecting to database: {err}")
        print("Error detected: Database connection issue.")
        return None

def is_rate_limited(username):
    """
    Check if a user has exceeded login attempts within a time frame to prevent abuse.
    Allows a maximum of 5 attempts in 60 seconds.
    """
    current_time = time()
    
    # If it's the first attempt, initialize tracking
    if username not in login_attempts:
        login_attempts[username] = [current_time]
        return False
    
    # Remove outdated login attempts older than 60 seconds
    login_attempts[username] = [t for t in login_attempts[username] if current_time - t < 60]

    # Block login if 5 attempts were made in the last 60 seconds
    if len(login_attempts[username]) >= 5:
        return True
    
    # Store this attempt and allow login attempt
    login_attempts[username].append(current_time)
    return False

def generate_card():
    """
    Generate a random playing card from predefined suits and values.
    """
    return random.choice(values) + " of " + random.choice(suits)

def hash_password(password):
    """
    Hash a password using bcrypt with an additional playing card-based salt.
    This enhances security by adding an unpredictable component to passwords.
    """
    extra_salt = random.choice(values) + random.choice(suits)  # Generates a random card as salt
    salted_password = password + extra_salt  # Appends card information to password before hashing
    return bcrypt.hashpw(salted_password.encode(), bcrypt.gensalt()), extra_salt

def verify_password(stored_hash, entered_password, extra_salt):
    """
    Validate a password by combining the stored salt and checking against the hashed version.
    """
    salted_password = entered_password + extra_salt  # Append salt before verification
    return bcrypt.checkpw(salted_password.encode(), stored_hash.encode())  # Verify hashed password

def login(username, password):
    """
    Authenticate the user with rate limiting, card verification challenge, and secure password comparison.
    """
    try:
        # Validate input types and length restrictions
        if not isinstance(username, str) or not isinstance(password, str):
            raise ValueError("Invalid input type. Username and password must be strings.")
        if len(username) > 20 or len(password) > 20:
            raise ValueError("Input too long. Username and password must be less than 20 characters.")

        # Apply rate limiting check
        if is_rate_limited(username):
            print(f"Rate limit exceeded for user {username}. Please try again later.")
            return False

        # Generate a security challenge using a random playing card
        card = generate_card()
        print(f"For additional security, identify this card: {card}")
        user_card = input("Enter the card shown: ")

        # If the user enters the wrong card, reject login
        if user_card.strip() != card:
            print("Card verification failed.")
            return False

        # Connect to the database for user authentication
        conn = connect_to_database()
        if not conn:
            return False

        cursor.execute("SELECT password, salt FROM users WHERE username = %s", (username,))

        cursor = conn.cursor()
        cursor.execute("SELECT password, salt FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()  # Retrieve user credentials

        # Check if the password matches the stored hashed password
        if result and verify_password(result[0], password, result[1]):
            print(f"Login successful! Welcome, {username}.")
            return True
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
            conn.close()  # Close database connection after login attempt
    
    return False

def card_sort_and_search():
    """
    Generates all 52 playing cards, sorts them alphabetically, and prints the sorted list.
    """
    try:
        cards = [value + " of " + suit for suit in suits for value in values]  # Generate full deck
        sorted_cards = sorted(cards)  # Sort deck
        print("Sorted cards:", sorted_cards)
    except Exception as e:
        logging.error(f"Error during card sort and search: {e}")
        print("Error detected: Card sorting failed.")

# Main execution logic
try:
    input_username = input("Enter your username: ")
    input_password = input("Enter your password: ")

    # Attempt login and proceed to card operations if successful
    if login(input_username, input_password):
        card_sort_and_search()
except Exception as ex:
    logging.error(f"Error during user input: {ex}")
    print("Error detected: An unexpected error occurred.")
