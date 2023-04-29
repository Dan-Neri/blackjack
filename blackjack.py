"""This simulator will play out a certain number of blackjack hands 
according to basic blackjack strategy and give stats on the number of 
hands won/lost as well as the total amount of money won/lost. Useful for
testing out different betting strategies.
"""
import random

import deck

class Shoe(deck.Deck):
    """This class represents a dealer shoe containing multiple decks of
    cards and inherits from Deck.
    """
    
    def __init__(self, decks=6):
        """Create a shoe containing all of the cards from the specified 
        number of decks instead of a single deck.
        """
        self.numberOfDecks = decks
        self.suits = ['C', 'D', 'H', 'S']
        self.ranks = [
            'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'
        ]
        self.cards = []
        for i in range(decks):
            for suit in self.suits:
                for rank in self.ranks:
                    self.cards.append([rank, suit])
    
    def shuffle(self):
        """Shuffle all cards back into the shoe"""
        self.__init__(self.numberOfDecks)
        random.shuffle(self.cards)
    
    def __str__(self):
        """Return a string representation of this Shoe"""
        message = f"A {self.numberOfDecks}-deck shoe containing "
        message += f"{len(self.cards)} cards"
        return message


class Hand():
    """This class represents one blackjack hand."""
    
    def __init__(self):
        """Initialize a new Hand with no cards in it."""
        self.cards = []
        self.total = 0
        self.bust = False
        self.bj = False
        self.soft = False
    
    def calculate_total(self):
        """Calculate the total of this Hand and trip any appropriate flags."""
        value = 0
        faces =['J', 'Q', 'K']
        for card in self.cards:
            try:
                value += int(card[0])
            except ValueError:
                if card[0] == 'A':
                    if value+11 > 21:
                        value += 1
                    else:
                        value += 11
                        self.soft = True
                elif any(x in card[0] for x in faces):
                    value += 10
            if value == 21 and len(self.cards) == 2:
                self.bj = True
                self.soft = False
            elif value > 21:
                if self.soft:
                    value -= 10
                    self.soft = False
                else:
                    self.bust = True     
        self.total = value
        
    def add_card(self, card):
        """Add card to this Hand."""
        self.cards.append(card)
        self.calculate_total()
        
    def discard(self):
        """Discard all cards in this Hand."""
        self.__init__()
        
    def __str__(self):
        """Return a string containing the cards in this Hand and the total."""
        message = ''
        for card in self.cards:
            message += card[0] + card[1] + ' '
            
        message += f"\nTotal: {self.total}"
        return message
    

class Player():
    """This class represents a blackjack player."""
    
    def __init__(self, name="player", bank=100, bet=10):
        """Initialize a new player with one empty hand"""
        self.name = name
        self.bank = bank
        self.bet = bet
        self.hands = [Hand()]