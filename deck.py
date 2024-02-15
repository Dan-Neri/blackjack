import random

class Deck:
    """A class representing a standard deck of 52 playing cards"""
    SUITS = ['C', 'D', 'H', 'S']
    RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self):
        """Initialize a new Deck.
        
        Each card is represented as a list in the form [rank, suit].
        """
        self.cards = []
        for suit in Deck.SUITS:
            for rank in Deck.RANKS:
                self.cards.append([rank, suit])
        
    def shuffle(self) -> None:
        """Shuffle all cards back into the Deck."""
        self.__init__()
        random.shuffle(self.cards)
        
    def shuffle_remaining(self) -> None:
        """Shuffle only the cards that have not been dealt already."""
        random.shuffle(self.cards)
        
    def deal(self) -> list[str]:
        """Remove the last card in the deck and return it."""
        return self.cards.pop()
        
    def count(self) -> int:
        """return the number of cards left in the deck."""
        return len(self.cards)
        
    def reveal(self) -> None:
        """Print a string list of all cards left in the deck."""
        message = ''
        for card in self.cards:
            message += card[0] + card[1] + ' '
        print(message)
        
    def __str__(self) -> str:
        """Return a string description of this deck."""
        return (f"A deck of {len(self.cards)} cards")


if __name__ == '__main__':
    myDeck = Deck()
    myDeck.shuffle()
    print('New deck shuffled')
    print('Dealing 5 cards')
    for i in range(5):
        print(myDeck.deal())
    print(myDeck)
    print(myDeck.cards)
    

