import random
import secrets

def main():
    # Step 1: Create and securely shuffle the deck
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [f"{value} of {suit}" for suit in suits for value in values]

    # Securely shuffle the deck using cryptographic randomness
    random_gen = secrets.SystemRandom()
    random_gen.shuffle(deck)

    # Step 2: Validate Player Names
    player1_name = input("Enter name for Player 1: ").strip()[:20]  # Limit input length
    player2_name = input("Enter name for Player 2: ").strip()[:20]  # Prevent excessively long input

    # Ensure names are not empty
    if not player1_name or not player2_name:
        print("Error: Player names cannot be empty!")
        return

    # Step 3: Handle Empty Deck Scenario
    if len(deck) < 2:
        print("Error: Insufficient cards left in the deck. Restarting game.")
        return

    try:
        player1_card = deck.pop()
        player2_card = deck.pop()
    except IndexError:
        print("Error: The deck is empty!")
        return

    print(f"{player1_name} drew {player1_card}")
    print(f"{player2_name} drew {player2_card}")

    # Step 4: Determine card values with error handling
    def get_card_value(card):
        try:
            value = card.split()[0]
            value_map = {
                '2': 2, '3': 3, '4': 4, '5': 5,
                '6': 6, '7': 7, '8': 8, '9': 9,
                '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
            }
            return value_map.get(value, 0)  # Ensures default value is returned if an error occurs
        except Exception as e:
            print(f"Error extracting card value: {e}")
            return 0  # Safe fallback value

    player1_value = get_card_value(player1_card)
    player2_value = get_card_value(player2_card)

    # Step 5: Decide winner
    if player1_value > player2_value:
        winner = player1_name
        print(f"{player1_name} wins!")
    elif player1_value < player2_value:
        winner = player2_name
        print(f"{player2_name} wins!")
    else:
        winner = "Tie"
        print("It's a tie game!")

    # Step 6: Securely log game results
    def log_game_result(player1_name, player1_card, player2_name, player2_card, winner):
        try:
            with open("game_results.log", "a") as log_file:
                log_file.write(f"{player1_name} drew {player1_card}, {player2_name} drew {player2_card} - {winner} won\n")
        except IOError as e:
            print(f"Error logging game result: {e}")

    log_game_result(player1_name, player1_card, player2_name, player2_card, winner)

if __name__ == "__main__":
    main()
