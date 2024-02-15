class Hand:
    """This class represents one blackjack hand."""
    SUITS = ['C', 'D', 'H', 'S']
    RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    TENS = ['10', 'J', 'Q', 'K']
    
    def __init__(self, card1: list[str] = None, card2: list[str] = None):
        """Initialize a new Hand.
        
        cards holds a list of all the cards in the hand. By default a Hand is
        created with no cards in it. options holds a list of valid blackjack
        moved based on the cards in this hand. The flags bust, bj, and soft
        indicate whether the Hand has a total over 21, exactly 21 with 2 cards,
        or an ace that is being counted with a value of 11 respectively. The
        double multiplier indicates whether this hand is worth double the bet 
        or not.
        
        Keyword arguments:
        card1   --  The first card in the Hand. Cards should be a list of
                    strings in the form [rank, suit]. (None default)
        card2   --  The second card in the Hand. (None default)
        """
        self.total = 0
        self.bust = False
        self.bj = False
        self.soft = False
        self.double = 1
        self.options = []
        self.cards = []
        if card1 and card2:
            if (
                    card1[0] not in Hand.RANKS or
                    card1[1] not in Hand.SUITS or
                    card2[0] not in Hand.RANKS or 
                    card2[1] not in Hand.SUITS
            ):
                print('Invalid format.', end=' ')
                print('Cards must be in the format [rank, suit]')
                print('New hand created with no cards')
            else:
                self.cards = [card1, card2]
        elif card1 or card2:
            print('Only allowed to create a hand with 2 cards or no cards')
            print('New hand created with no cards')
        self.set_options()
        
    def calculate_total(self) -> None:
        """Calculate the total of this Hand and trip the appropriate flags."""
        total = 0
        for card in self.cards:
            if card[0] == 'A':
                if total+11 > 21:
                    total += 1
                else:
                    total += 11
                    self.soft = True
            elif card[0] in Hand.TENS:
                total += 10
            else:
                total += int(card[0])
            if total == 21 and len(self.cards) == 2:
                self.bj = True
                self.soft = False
            elif total > 21:
                if self.soft:
                    total -= 10
                    self.soft = False
                else:
                    self.bust = True
        self.total = total
        
    def add_card(self, card: list[str]) -> None:
        """Add a card to this Hand. Recalculate the available options.
        
        Keyword arguments:
        card    --  The card to be added to the hand. Card should be a list of
                    strings in the form [rank, suit].
        """
        if (card[0] not in Hand.RANKS) or (card[1] not in Hand.SUITS):
            print('Invalid format. Cards must be in the format [rank, suit]')
        self.cards.append(card)
        self.set_options()
                
    def discard(self, index: int = -1) -> None:
        """Discard a card from the Hand.
        
        Keyword arguments:
        index   --  The index of the card to discard. If index is -1, the most
                    recently dealt card will be discarded. (-1 default)
        """
        if self.cards:
            self.cards.pop(index)
            self.set_options()
        else:
            print('Cannot discard from an empty hand')
            
    def set_options(self) -> None:
        """Populate valid options based on the current cards in the Hand."""
        self.calculate_total()
        self.options = []
        if self.total < 21 and self.bust == False:
            self.options.append('s')
            self.options.append('stand')
            self.options.append('h')
            self.options.append('hit')
            if len(self.cards) == 2:
                self.options.append('d')
                self.options.append('double')
                if(
                        self.cards[0][0] == self.cards[1][0] or
                        (self.cards[0][0] in Hand.TENS and 
                        self.cards[1][0] in Hand.TENS)
                ):
                    self.options.append('p')
                    self.options.append('split')
    
    def str_card(self, index: int = 0):
        """Return a String representing a specific card in this Hand. 
        
        If an invalid index is provided, an 'X' is returned instead.
        
        Keyword arguments:
        index   --  The index of the card to be returned.
        """
        message = ''
        if index >= len(self.cards):
            message += 'X'
        else:
            message += f'{self.cards[index][0]}{self.cards[index][1]}'
        return message
        
    def str_options(self) -> str:
        """Return a user friendly string of valid options for this Hand."""
        message = ''
        if 's' in self.options:
            message += '(S)tand'
        if 'h' in self.options:
            message += ' (H)it'
        if 'd' in self.options:
            message += ' (D)ouble'
        if 'p' in self.options:
            message += ' S(p)lit'
        return message
        
    def __str__(self) -> str:
        """Return a string including cards, total, and flags for this Hand."""
        message = ''
        for card in self.cards:
            message += card[0] + card[1] + ' '
        message += f' Total: {self.total}'
        if self.bust:
            message += ' (BUST)'
        elif self.bj:
            message += ' (BLACKJACK)'
        elif self.soft:
            message += ' (SOFT)'
        return message


if __name__ == '__main__':
    myHand = Hand(['A', 'H'], ['A', 'S'])
    print(myHand)
    myHand.add_card(['10', 'C'])
    print(myHand.options)
    print(myHand.str_options())
    print(myHand)
    print(myHand.cards)
    print(myHand.cards[0])
    print(myHand.str_card(0))
    print(myHand.total)