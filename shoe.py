import random

from deck import Deck

class Shoe(Deck):
    """This class represents a dealer shoe containing multiple decks of
    cards and inherits from Deck.
    """
    
    def __init__(self, decks: int = 6):
        """Create a shoe containing the specified number of Decks.
        
        A random value between 52 and 104, the size of one to two decks, is
        chosen upon initialization and stored as cutCard. Once the remaining
        number of cards in the shoe reaches the cutCard value, the shuffleFlag
        is set to True. This flag indicates that the shoe should be shuffled.
        The shoe is not shuffled immediately when this flag is tripped to allow
        the current hand to be completed first.
        """
        self.numberOfDecks = decks
        self.cutCard = random.randint(52, 104)
        self.shuffleFlag = False
        self.cards = []
        for i in range(decks):
            for suit in Deck.SUITS:
                for rank in Deck.RANKS:
                    self.cards.append([rank, suit])
    
    def shuffle(self) -> None:
        """Shuffle all cards back into the shoe."""
        self.__init__(self.numberOfDecks)
        random.shuffle(self.cards)
    
    def deal(self) -> list[str]:
        """Remove the last card in the deck and return it."""
        if len(self.cards) == self.cutCard:
            self.shuffleFlag = True
        return self.cards.pop()
    
    def __str__(self) -> str:
        """Return a string representation of this Shoe."""
        message = f"A {self.numberOfDecks}-deck shoe containing "
        message += f"{len(self.cards)} cards"
        return message


if __name__ == '__main__':
    myShoe = Shoe()
    myShoe.shuffle()
    print(f'Shuffled myShoe, {myShoe}')
    print('Dealing 10 cards:')
    for i in range(10):
        print(myShoe.deal())
    print(f'myShoe: {myShoe}')
    