import random
import secrets
import hashlib
import re

# Function to encrypt player names using SHA-256 hashing
def encrypt_name(name):
    """Encrypt the player name using SHA-256 hashing to protect sensitive player data."""
    return hashlib.sha256(name.encode()).hexdigest()

# Function to sanitize input to prevent excessive length (DoS) and buffer overflow risks
def sanitize_input(user_input, max_length=20):
    """Sanitize input by limiting the length to prevent denial-of-service attacks."""
    return user_input[:max_length].strip()

# Function to sanitize user input to prevent command injection
def secure_input(user_input):
    """Sanitize input to prevent command injection by allowing only alphanumeric characters."""
    return re.sub(r'[^a-zA-Z0-9 ]', '', user_input)

# Function to mask data before logging to prevent data leakage
def mask_data(data):
    """Mask sensitive data before logging to avoid exposing plaintext information."""
    return "*" * len(data)

def main():
    # Step 1: Create and shuffle the deck
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    
    # Creating a full deck of cards
    deck = [f"{value} of {suit}" for suit in suits for value in values]
    
    # Securely shuffling the deck using a cryptographically secure random function
    secrets.SystemRandom().shuffle(deck)

    # Step 2: Players draw a card with secured and sanitized input
    player1_name = secure_input(sanitize_input(input("Enter name for Player 1: ")))  # Sanitization applied
    player2_name = secure_input(sanitize_input(input("Enter name for Player 2: ")))  # Sanitization applied

    # Encrypt player names before storing or transmitting
    player1_encrypted = encrypt_name(player1_name)
    player2_encrypted = encrypt_name(player2_name)

    try:
        # Players pick a random card from the shuffled deck
        player1_card = deck.pop()
        player2_card = deck.pop()
    except IndexError:
        print("Error: The deck is empty!")  # Prevents crashes due to an empty deck
        return

    print(f"{player1_name} drew {player1_card}")
    print(f"{player2_name} drew {player2_card}")

    # Step 3: Determine card values
    def get_card_value(card):
        """Extract card value and map it to numerical representation for comparison."""
        value = card.split()[0]
        value_map = {
            '2': 2, '3': 3, '4': 4, '5': 5,
            '6': 6, '7': 7, '8': 8, '9': 9,
            '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
        }
        return value_map.get(value, 0)  # Default to 0 for unexpected values

    player1_value = get_card_value(player1_card)
    player2_value = get_card_value(player2_card)

    # Decide winner
    if player1_value > player2_value:
        print(f"{player1_name} wins!")
    elif player1_value < player2_value:
        print(f"{player2_name} wins!")
    else:
        print("It's a tie game!")

    # Logging secured data with masking applied (instead of plaintext logging)
    print(f"Logging secured data: {mask_data(player1_name)}, {mask_data(player2_name)}")

    # Display encrypted player names for security purposes
    print(f"Encrypted Player 1: {player1_encrypted}")
    print(f"Encrypted Player 2: {player2_encrypted}")

# Ensures the script runs only if executed directly, preventing unintended execution if imported
if __name__ == "__main__":
    main()
