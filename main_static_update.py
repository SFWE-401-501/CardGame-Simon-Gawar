import random  # Standard Python library for random number generation
import secrets  # Cryptographic module for secure randomization

def main():
    """
    Main function to run the card game between two players.
    """

    # Step 1: Create and securely shuffle the deck
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']  # Defines the four suits of a standard deck
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']  # Defines the card values

    # Generate a full deck by combining each value with each suit
    deck = [f"{value} of {suit}" for suit in suits for value in values]

    # Securely shuffle the deck using cryptographic randomness to prevent predictability
    random_gen = secrets.SystemRandom()
    random_gen.shuffle(deck)

    # Step 2: Validate Player Names
    player1_name = input("Enter name for Player 1: ").strip()[:20]  # Limits input length to prevent buffer overflow
    player2_name = input("Enter name for Player 2: ").strip()[:20]  # Ensures input does not exceed a reasonable length

    # Ensure names are not empty
    if not player1_name or not player2_name:
        print("Error: Player names cannot be empty!")  # Displays an error message for invalid input
        return  # Stops execution to prevent undefined variables

    # Step 3: Handling Empty Deck Scenario
    if len(deck) < 2:  # Check if the deck contains enough cards for both players
        print("Error: Insufficient cards left in the deck. Restarting game.")  # Warns the user
        return  # Stops execution safely

    try:
        # Players draw a card from the shuffled deck
        player1_card = deck.pop()
        player2_card = deck.pop()
    except IndexError:  # Catches potential errors when drawing from an empty deck
        print("Error: The deck is empty!")  # Displays a controlled error message
        return  # Stops execution gracefully

    # Show each player's drawn card
    print(f"{player1_name} drew {player1_card}")
    print(f"{player2_name} drew {player2_card}")

    # Step 4: Determine card values with error handling
    def get_card_value(card):
        """
        Extracts the numerical value of a card based on predefined rankings.
        """
        try:
            value = card.split()[0]  # Retrieves the first part of the card string (e.g., "10", "J", "A")
            value_map = {
                '2': 2, '3': 3, '4': 4, '5': 5,
                '6': 6, '7': 7, '8': 8, '9': 9,
                '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14  # Assigns numerical ranks to face cards
            }
            return value_map.get(value, 0)  # Ensures default value (0) is returned in case of unexpected input
        except Exception as e:  # Catches any error in case card value extraction fails
            print(f"Error extracting card value: {e}")  # Logs the error to console
            return 0  # Returns a safe default value

    # Compute numerical values for each player's drawn card
    player1_value = get_card_value(player1_card)
    player2_value =