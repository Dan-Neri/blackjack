"""This is a simulation which will play out the given number of blackjack hands
between a player and a dealer according to basic blackjack strategy and give
stats based on the number of hands won, lost, and overall money won or lost"""
import random
import itertools

class Cards:
    """This class contains a number of different methods for dealing with
    a deck of cards"""
    
    def __init__(self, players=2):
        """Initializes a new deck and a number of players with empty hands"""     
        self.deck = self.new_deck() 
        self.hands = []
        
        for p in range(players):
            self.hands.insert(p, [])
        
        print(f"A new game of cards with {players} player(s) has been started")
            
    def new_deck(self):
        """Returns a list containing a representation of a standard deck of
        cards"""
        FACE_CARDS = ('J', 'Q', 'K', 'A')
        SUITS = ('H', 'D', 'C', 'S')
        
        return list(itertools.product(
            itertools.chain(range(2,11), FACE_CARDS),
            SUITS
            )
        )
        
    def show_deck(self):
        """Prints the remaining cards the deck"""
        print(f"There are {len(self.deck)} cards remaining in the deck: ")
        for card in self.deck:
            print("{:>2}{}".format(*card), end=' ')
        print("\r")
    
    def shuffle_deck(self):
        """Sets the deck to a newly shuffled deck of 52 cards"""
        self.deck = self.new_deck()
        random.shuffle(self.deck)
        self.discard_hands()
        print("The deck has been shuffled")
        
    def shuffle_remaining_deck(self):
        """Shuffles only the remaining cards in the deck. Does not suffle
        already used cards back in"""
        random.shuffle(self.deck)
        print("The remaining cards have been shuffled")
        
    def show_hands(self):
        """Prints the players current hands"""
        for i in range(len(self.hands)):
            if self.hands[i]:
                print(f"Player {i + 1}:", end=' ')
                for card in self.hands[i]:
                    print("{:>2}{}".format(*card), end=' ')
                print("\r")
            else:
                print("Empty")
      
    def deal(self, number):
        """Deals out the specified number of cards to each player"""
        print(f"Dealing {number} card(s) to each player")
        if number * len(self.hands) > len(self.deck):
            print(
                f"There are not enough cards left in the deck to deal {number}" 
                + " card(s) to each player")
        else:
            for n in range(number):
                for hand in self.hands:
                    hand.append(self.deck.pop())

    def discard_hands(self):
        """Discards the cards in all players hands"""
        print("Discarding all players hands")
        for i in range(len(self.hands)):
            self.hands[i] = []

    def set_players(self, players=2):
        """sets the number of players in the game. This will also discard any
        cards in the current players hands and shuffle a new deck"""
        self.hands = []
        for p in range(players):
            self.hands.insert(p, [])
        print(f"The number of players has been set to {players}")
        self.shuffle_deck()