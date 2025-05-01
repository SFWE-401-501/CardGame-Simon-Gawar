import random

def main():
    # Step 1: Create and shuffle the deck
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [f"{value} of {suit}" for suit in suits for value in values]
    random.shuffle(deck)

    # Step 2: Players draw a card
    player1_name = "Player 1"
    player2_name = "Player 2"

    player1_card = deck.pop()
    player2_card = deck.pop()

    print(f"{player1_name} drew {player1_card}")
    print(f"{player2_name} drew {player2_card}")

    # Step 3: Determine card values
    def get_card_value(card):
        value = card.split()[0]
        value_map = {
            '2': 2, '3': 3, '4': 4, '5': 5,
            '6': 6, '7': 7, '8': 8, '9': 9,
            '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
        }
        return value_map[value]

    player1_value = get_card_value(player1_card)
    player2_value = get_card_value(player2_card)

    # Step 4: Decide winner
    if player1_value > player2_value:
        print(f"{player1_name} wins!")
    elif player1_value < player2_value:
        print(f"{player2_name} wins!")
    else:
        print("It's a tie game!")

if __name__ == "__main__":
    main()
