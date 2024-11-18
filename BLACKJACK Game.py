

# WELCOME TO BLACKJACK GAME CODE, IF YOU HAVE NO IDEA WHAT IS A BLACKJACK GAME, PLEASE CHECK IT OUT IN GOOGLE


# let's import Random library
import random

# Card Suits, Ranks, and Values
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

# Classes
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in suits for rank in ranks]

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:
    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

# Functions
def ask_to_bet():
    """
    Ask the player if they would like to place a bet before proceeding.
    """
    while True:
        response = input("Would you like to place a bet? (yes/no): ").strip().lower()
        if response == 'yes':
            return True  # Proceed to place a bet
        elif response == 'no':
            print("You must place a bet to play. Please reconsider.")
        else:
            print("Invalid input. Please type 'yes' to place a bet or 'no' to exit.")


def take_bet(chips):
    """
    Prompt the player to place a bet after confirming their willingness.
    """
    while True:
        try:
            print(f"\nYou currently have {chips.total} chips.")
            chips.bet = int(input("How many chips would you like to bet? "))
            if chips.bet <= 0:
                print("Invalid bet! You must bet more than zero.")
            elif chips.bet > chips.total:
                print("Insufficient chips! You cannot bet more than your total chips.")
            else:
                print(f"Bet accepted: {chips.bet} chips.")
                break
        except ValueError:
            print("Invalid input! Please enter a valid number.")


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    while True:
        choice = input("Would you like to Hit or Stand? (hit/stand): ").strip().lower()
        if choice == 'hit':
            hit(deck, hand)
            return True  # Continue playing
        elif choice == 'stand':
            print("Player stands. Dealer's turn.")
            return False  # Stop playing
        else:
            print("Invalid input. Please type 'hit' or 'stand'.")


def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')


def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)


def player_busts(chips):
    print("Player busts!")
    chips.lose_bet()


def player_wins(chips):
    print("Player wins!")
    chips.win_bet()


def dealer_busts(chips):
    print("Dealer busts!")
    chips.win_bet()


def dealer_wins(chips):
    print("Dealer wins!")
    chips.lose_bet()


def push():
    print("It's a tie! Push.")

# Main Game Loop
while True:
    print("Welcome to Blackjack! Try to get as close to 21 as possible without going over.\n")
    
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    dealer_hand = Hand()
    
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    
    player_chips = Chips()
    
    # Ask if the player wants to place a bet
    if ask_to_bet():
        take_bet(player_chips)
    
    show_some(player_hand, dealer_hand)
    
    playing = True
    while playing:
        playing = hit_or_stand(deck, player_hand)
        show_some(player_hand, dealer_hand)
        if player_hand.value > 21:
            player_busts(player_chips)
            break
    
    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)
        show_all(player_hand, dealer_hand)
        
        if dealer_hand.value > 21:
            dealer_busts(player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_chips)
        else:
            push()
    
    print(f"\nPlayer's total chips: {player_chips.total}")
    new_game = input("Would you like to play again? (y/n): ").strip().lower()
    if new_game != 'y':
        print("Thanks for playing! Goodbye!")
        break
