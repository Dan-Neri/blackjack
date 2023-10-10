import random

class Deck:
    """A class representing a standard deck of 52 playing cards"""

    def __init__(self):
        """Initialize a new Deck with each card represented as a list in the
        form [rank, suit]"""
        self.suits = ['C', 'D', 'H', 'S']
        self.ranks = [
            'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'
        ]
        self.cards = []
        for suit in self.suits:
            for rank in self.ranks:
                self.cards.append([rank, suit])
        
    def shuffle(self):
        """Shuffle all cards back into the Deck"""
        self.__init__()
        random.shuffle(self.cards)
        
    def shuffle_remaining(self):
        """Shuffle only the cards remaining deck"""
        random.shuffle(self.cards)
        
    def deal(self):
        """Remove the last card in the deck and return it"""
        return self.cards.pop()
        
    def count(self):
        """return the number of cards left in the deck"""
        return len(self.cards)
        
    def reveal(self):
        """Print a string list of all cards left in the deck"""
        message = ''
        for card in self.cards:
            message += card[0] + card[1] + ' '
        print(message)
        
    def __str__(self):
        """Return a string description of this deck"""
        return (f"A deck of {len(self.cards)} cards")



