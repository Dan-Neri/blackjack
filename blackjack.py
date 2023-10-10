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
        number of decks instead of a single deck. A random cutCard is
        also chosen to indicate when the shoe should be shuffled.
        """
        self.numberOfDecks = decks
        self.cutCard = random.randint(52, 104)
        self.shuffleFlag = False
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
    
    def deal(self):
        """Remove the last card in the deck and return it. Check to see
        if the cut card has been dealt"""
        if len(self.cards) == self.cutCard:
            print("The cut card has been dealt. Shoe will be shuffled " +
            "after this hand")
            self.shuffleFlag = True
        return self.cards.pop()
    
    def __str__(self):
        """Return a string representation of this Shoe"""
        message = f"A {self.numberOfDecks}-deck shoe containing "
        message += f"{len(self.cards)} cards"
        return message


class Hand:
    """This class represents one blackjack hand."""
    
    def __init__(self, card1=None, card2=None):
        """Initialize a new Hand"""
        self.total = 0
        self.bust = False
        self.bj = False
        self.soft = False
        self.double = 1
        self.options = []
        if card1 and card2:
            self.cards = [card1, card2]
        elif card1 or card2:
            print("Only allowed to create a hand with 2 cards or no cards")
            print("New hand created with no cards")
        else:
            self.cards = []
        self.get_options()
        
    def calculate_total(self):
        """Calculate the total of this Hand and trip the appropriate flags"""
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
        """Add a card to this Hand"""
        self.cards.append(card)
        self.get_options()
                
    def get_card(self, position=0):
        """Return a String representing a specific card in this Hand. If
        an invalid index is provided, return an 'X' instead.
        """
        message = ''
        if position >= len(self.cards):
            message += 'X'
        else:
            message += f"{self.cards[position][0]}{self.cards[position][1]}"
        return message
        
    def get_options(self):
        """Populate self.options based on the current cards in the Hand"""
        self.calculate_total()
        self.options = []
        if self.total < 21 and self.bust == False:
            self.options.append('s')
            self.options.append("stand")
            self.options.append('h')
            self.options.append("hit")
            if len(self.cards) == 2:
                self.options.append('d')
                self.options.append("double")
                if(self.cards[0][0] == self.cards[1][0]):
                    self.options.append("sp")
                    self.options.append("split")
                    
    def str_options(self):
        """Return a user friendly string of available options for this Hand"""
        message = ''
        if 's' in self.options:
            message += "(S)tand"
        if 'h' in self.options:
            message += " (H)it"
        if 'd' in self.options:
            message += " (D)ouble"
        if "sp" in self.options:
            message += " (Sp)lit"
        return message
        
    def __str__(self):
        """Return a string containing the cards in this Hand and the total."""
        message = ''
        for card in self.cards:
            message += card[0] + card[1] + '  '
        message += f"Total: {self.total}"
        if self.bust:
            message += " BUST"
        elif self.bj:
            message += " BLACKJACK"
        elif self.soft:
            message += " SOFT"
        return message
    

class Player:
    """This class represents a blackjack player."""
    
    def __init__(self, name="player", bet=10, bank=100):
        """Initialize a new player with one empty hand"""
        self.name = name
        self.bank = bank
        self.bet = bet
        self.hands = [Hand()]
        
    def set_name(self, name):
        """Update a Player's name"""
        self.name = name
        
    def set_bank(self, amount):
        """Update a Player's bank"""
        self.bank = amount
        
    def set_bet(self, amount):
        """Update a Player's bet"""
        self.bet = amount
        
    def add_hand(self, hand=Hand()):
        """Add a new Hand to this Player"""
        self.hands.append(hand)
        
    def __str__(self):
        """Return a string representation of this Player"""
        return f"{self.name} - Bank: {self.bank} Bet: {self.bet}"


class Blackjack:
    """This class represents a game of blackjack and contains methods to
    help with the flow of the game.
    """
    
    def __init__(self, numberOfDecks=6, numberOfPlayers=1, minBet=10):
        """Create a new shoe and shuffle it. Create a Player
        representing the dealer and populate a list with the other
        Players.
        """
        self.minBet = minBet
        self.numberOfPlayers = numberOfPlayers
        self.numberOfDecks = numberOfDecks
        self.shoe = Shoe(numberOfDecks)
        self.shoe.shuffle()
        self.dealer = Player("Dealer")
        self.players = []
        for i in range(numberOfPlayers):
            self.players.append(Player(f"Player {i+1}", minBet))
        print(f"{self} has been started")
            
    def deal_round(self):
        """Add 2 cards to each Player's hand and the dealer's hand"""
        for player in self.players:
            player.hands[0].add_card(self.shoe.deal())
        self.dealer.hands[0].add_card(self.shoe.deal())
        for player in self.players:
            player.hands[0].add_card(self.shoe.deal())
        self.dealer.hands[0].add_card(self.shoe.deal())
        
    def show_hands(self):
        """Print each player's hand, but only show the first card of the
        dealer's hand"""
        for player in self.players:
            message = f"{player.name}: "
            for hand in player.hands:
                message += f"{hand}\r"
            print(message)
                
        print(f"{self.dealer.name}: {self.dealer.hands[0].get_card()}\n")
        
    def calculate_winners(self):
        """Determine if each player """
        dHand = self.dealer.hands[0]
        for player in self.players:
            i = 0
            for hand in player.hands:
                i += 1
                print(player.name, end='')
                if dHand.bj and hand.bj:
                    print(f" ${player.bank}: pushed")
                elif hand.bj:
                    player.bank += 1.5 * player.bet
                    print(f" ${player.bank}: won ${1.5*player.bet}")
                elif hand.bust:
                    player.bank -= player.bet * hand.double
                    print(f" ${player.bank}: lost ${player.bet*hand.double}")
                elif dHand.bust or dHand.total < hand.total:
                    player.bank += player.bet * hand.double
                    print(f" ${player.bank}: won ${player.bet*hand.double}")
                elif dHand.total > hand.total:
                    player.bank -= player.bet * hand.double
                    print(f" ${player.bank}: lost ${player.bet*hand.double}")
                elif hand.total == dHand.total:
                    print(f" ${player.bank}: pushed")
    
    def play_dealer(self):
        """Stand or hit for the dealer. Dealer hits on soft 17 and stands on
        all better hands"""
        hand = self.dealer.hands[0]
        active = True
        print(f"{self.dealer.name}:\n{hand}")
        while active:
            if hand.total > 17 or (hand.total == 17 and not hand.soft):
                active = False
            else:
                hand.add_card(self.shoe.deal())
                print(hand)
                
    def discard_hands(self):
        """Reinitialize hands for all players and the dealer"""
        for player in self.players:
            player.hands = [Hand()]
        self.dealer.hands = [Hand()]
        
    def check_ins(self):
        """Check to see if any player wants to take insurance. Return
        True if the dealer has blackjack and False otherwise"""
        dHand = self.dealer.hands[0]
        choices = ['y', "yes", 'n', "no"]
        if dHand.cards[0][0] == 'A':
            for player in self.players:
                invalid = True
                while invalid:
                    response = input(f"{player.name} ${player.bank}: " +
                        "Do you want to take insurance?").lower()
                    if response in choices:
                        invalid = False
                        if response == 'y' or response == "yes":
                            if not dHand.bj:
                                player.bank -= player.bet / 2
                        if response == 'n' or response == "no":
                            if dHand.bj:
                                player.bank -= player.bet
                    else:
                        print("Please respond with (Y)es or (N)o")
            if dHand.bj:
                print(f"{self.dealer.name} has blackjack")
            else:
                print(f"{self.dealer.name} doesn't have blackjack")
        return dHand.bj
            
    def play_round(self):
        """Deal cards then prompt each player to play their hand.
        Finish by playing the dealer's hand and paying the winners.
        """
        self.deal_round()
        self.show_hands()
        if not self.check_ins():
            for player in self.players:
                i = 0
                print(f"{player.name} ${player.bank-player.bet}: ", end = '')
                print(f"Bet ${player.bet}")
                # Allow a player to act on all hands
                while i < len(player.hands):
                    active = True
                    activeHand = player.hands[i]
                    print(player.hands[i])
                    # Keep prompting until this hand is completed
                    while active:
                        invalid = True
                        while invalid:
                            if activeHand.options:
                                strOptions = activeHand.str_options()
                                response = input(f"{strOptions}? ").lower()
                                if response in activeHand.options:
                                    invalid = False
                                else:
                                    print("Invalid action")
                            else:
                                invalid = False
                                active = False
                                response = ''
                        if response == 's' or response == "stand":
                            active = False
                        if response == 'h' or response == "hit":
                            activeHand.add_card(self.shoe.deal())
                            print(activeHand)
                            if activeHand.bj or activeHand.bust:
                                active = False
                        elif response == 'd' or response == "double":
                            if player.bank < player.bet*2:
                                activeHand.options.remove('d')
                                activeHand.options.remove("double")
                                activeHand.add_card(self.shoe.deal())
                                print("Not enough money to double down")
                            else:
                                activeHand.double = 2
                                activeHand.add_card(self.shoe.deal())
                                print(activeHand)
                                active = False
                        elif response == 'sp' or response == 'split':
                            if len(player.hands) < 4:
                                newHand = Hand(
                                    activeHand.cards[1], 
                                    self.shoe.deal()
                                )
                                activeHand.cards[1] = self.shoe.deal()
                                newHand.get_options()
                                activeHand.get_options()
                                # Only allowed to stand or split after
                                # splitting aces
                                if activeHand.cards[0][0] == 'A':
                                    activeHand.options = []
                                    newHand.options = []
                                    if (activeHand.cards[1][0] == 'A' and 
                                            len(player.hands) < 3):
                                        activeHand.options.append('s')
                                        activeHand.options.append("stand")
                                        activeHand.options.append('sp')
                                        activeHand.options.append("split")
                                    if (newHand.cards[1][0] == 'A' and 
                                            len(player.hands) < 3):
                                        newHand.options.append('s')
                                        newHand.options.append("stand")
                                        newHand.options.append('sp')
                                        newHand.options.append("split")
                                player.hands[i] = activeHand
                                player.hands.append(newHand)
                                print(activeHand)
                            else:
                                print("You can only split a hand 3 times")
                    i += 1
        self.play_dealer()
        self.calculate_winners()
        self.discard_hands()
        if self.shoe.shuffleFlag:
            print("Shuffling shoe")
            self.shoe.shuffle()
            
    def __str__(self):
        """Return a string representation of this game"""
        message = f"A {self.numberOfDecks}-deck game of blackjack with "
        message += f"{self.numberOfPlayers} players"
        return message
        
        
myBJ = Blackjack(6,4)
game = True
menu = ['p', "play", "play a round", 'q', "quit"]
while game:
    invalid = True
    while invalid:
        response = input("Please select an option: (P)lay a round, " +
            "(Q)uit ").lower()
        if response in menu:
            invalid = False
            if response == 'p' or response.startswith("play"):
                myBJ.play_round()
            elif response == 'q' or response == "quit":
                game = False
        else:
            print("Invalid command")