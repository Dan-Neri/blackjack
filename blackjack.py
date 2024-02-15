"""This simulator will play out a certain number of blackjack hands 
according to basic blackjack strategy and give stats on the number of 
hands won/lost as well as the total amount of money won/lost. Useful for
testing out different betting strategies.
"""
from shoe import Shoe
from hand import Hand
from player import Player
from strategy import Strategy

class Blackjack:
    """This class represents a game of blackjack and contains methods to
    help with the flow of the game.
    """
    #Basic blackjack strategy for the player with a hard total and no option to
    #split. Chart legend: 's' = stand, 'h' = hit, 'p' = split
    #'dh' = double if possible hit otherwise, 
    #'ds' = double if possible stand otherwise.
    CHART = {
            4: ['h']*10,
            5: ['h']*10,
            6: ['h']*10,
            7: ['h']*10,
            8: ['h']*10,
            9: ['h'] + ['dh']*4 + ['h']*5,
            10: ['dh']*8 + ['h']*2,
            11: ['dh']*10,
            12: ['h']*2 + ['s']*3 + ['h']*5,
            13: ['s']*5 + ['h']*5,
            14: ['s']*5 + ['h']*5,
            15: ['s']*5 + ['h']*5,
            16: ['s']*5 + ['h']*5,
            17: ['s']*10,
            18: ['s']*10,
            19: ['s']*10,
            20: ['s']*10,
            21: ['s']*10
    }
    #Basic blackjack strategy for the player with a soft total and no option to
    #split.
    SOFTCHART = {
            12: ['h']*2 + ['s']*3 + ['h']*5,
            13: ['h']*3 + ['dh']*2 + ['h']*5,
            14: ['h']*3 + ['dh']*2 + ['h']*5,
            15: ['h']*2 + ['dh']*3 + ['h']*5,
            16: ['h']*2 + ['dh']*3 + ['h']*5,
            17: ['h'] + ['dh']*4 + ['h']*5,
            18: ['ds']*5 + ['s']*2 + ['h']*3,
            19: ['s']*4 + ['ds'] + ['s']*5,
            20: ['s']*10,
            21: ['s']*10
    }
    #Basic blackjack strategy for the player with an option to split.
    SPLITCHART = {
            '2s': ['p']*6 + ['h']*4,
            '3s': ['p']*6 + ['h']*4,
            '4s': ['h']*3 + ['p']*2 + ['H']*5,
            '5s': ['dh']*8 + ['h']*2,
            '6s': ['p']*5 + ['h']*5,
            '7s': ['p']*6 + ['h']*4,
            '8s': ['p']*10,
            '9s': ['p']*5 + ['s'] + ['p']*2 + ['s']*2,
            '10s': ['s']*10,
            'As': ['p']*10
    }
    
    def __init__(self, numberOfDecks: int = 6, numberOfPlayers: int = 1, 
            minBet: int = 10, maxBet: int = 1000):
        """Initialize the game with the given number of Players and options.
        
        Keyword arguments:
        numberOfDecks   --  The number of Decks to use in the dealer shoe.
                            (6 default)
        numberOfPlayers --  The number of Players in the game. (1 default)
        minBet          --  The minimum bet allowed in the game. (10 default)
        maxBet          --  The maximum bet allowed in the game. (1000 default)
        """
        self.minBet = minBet
        self.maxBet = maxBet
        self.numberOfPlayers = numberOfPlayers
        self.numberOfDecks = numberOfDecks
        self.shoe = Shoe(numberOfDecks)
        self.shoe.shuffle()
        self.dealer = Player('Dealer')
        self.players = []
        self.display = True
        for i in range(numberOfPlayers):
            self.players.append(Player(f'Player {i+1}', bet=minBet))
        print(f'{self} has been started')
            
    def deal_round(self) -> None:
        """Add 2 cards to each Player's Hand and the dealer's Hand."""
        for player in self.players:
            player.hands[0].add_card(self.shoe.deal())
        self.dealer.hands[0].add_card(self.shoe.deal())
        for player in self.players:
            player.hands[0].add_card(self.shoe.deal())
        self.dealer.hands[0].add_card(self.shoe.deal())
        
    def show_hands(self) -> None:
        """Print each player's hand, only print the dealer's first card."""
        for player in self.players:
            message = f'{player.name}: '
            for hand in player.hands:
                message += f'{hand}\r'
            print(message)
        print(f'{self.dealer.name}: ', end='') 
        print(f'{self.dealer.hands[0].str_card()}\n')
        
    def calculate_winners(self) -> None:
        """Calculate the result of each hand and adjust banks accordingly."""
        dHand = self.dealer.hands[0]
        for player in self.players:
            i = 0
            for hand in player.hands:
                i += 1
                bet = player.bet * hand.double
                if self.display:
                    print(player.name, end='')
                if dHand.bj and hand.bj:
                    if self.display:
                        print(f' ${player.bank}: pushed')
                elif hand.bj:
                    bet = player.bet * 1.5
                    player.win(bet)
                    if self.display:
                        print(f' ${player.bank}: won ${bet}')
                elif hand.bust:
                    player.lose(bet)
                    if self.display:
                        print(f' ${player.bank}: lost ${bet}')
                elif dHand.bust or dHand.total < hand.total:
                    player.win(bet)
                    if self.display:
                        print(f' ${player.bank}: won ${bet}')
                elif dHand.total > hand.total:
                    player.lose(bet)
                    if self.display:
                        print(f' ${player.bank}: lost ${bet}')
                elif hand.total == dHand.total and self.display:
                    print(f' ${player.bank}: pushed')
    
    def play_dealer(self) -> None:
        """Play the dealer's Hand.
        
        Dealer hits on soft 17 and stands on hard 17 and all better hands.
        """
        hand = self.dealer.hands[0]
        active = True
        if self.display:
            print(f'{self.dealer.name}:\n{hand}')
        while active:
            if (
                    hand.total > 17 or 
                    (hand.total == 17 and not hand.soft)
            ):
                active = False
            else:
                hand.add_card(self.shoe.deal())
                if self.display:
                    print(hand)
                    
    def play_hand(self, player: Player) -> None:
        """Play a Player's Hand automatically according to basic strategy.
        
        CHART, SOFTCHART, and SPLITCHART can be modified to adjust how these
        Hands are played.
        """
        upCard = self.dealer.hands[0].cards[0]
        i = 0
        currentBets = 1
        bet = player.bet
        bank = player.bank
        if not upCard:
            print('Can\'t play hand. Please deal a round first.')
            return
        else:
            if upCard[0] in Hand.TENS:
                upCardIndex = 8
            elif upCard[0] == 'A':
                upCardIndex = 9
            else:
                upCardIndex = int(upCard[0]) - 2
        if self.dealer.hands[0].total == 21:
            return
        #Loop for each hand the player has. Allows for splitting.
        while i < len(player.hands):
            active = True
            activeHand = player.hands[i]
            if self.display:
                print(f'{player.name}: {activeHand}')
            #Keep looping until this hand is completed.
            while active:
                #Remove double option if the bank is too low.
                if 'd' in activeHand.options:
                    if bank < ((currentBets*bet) + bet):
                        activeHand.options.remove('d')
                        activeHand.options.remove('double')
                #Remove split option if the bank is too low or the Hand has
                #already been split 3 times.
                if 'p' in activeHand.options:
                    if (
                            bank < ((currentBets*bet) + bet) or
                            len(player.hands) >= 4
                    ):
                        activeHand.options.remove('p')
                        activeHand.options.remove('split')
                #Check if this Hand can be split.
                if 'p' in activeHand.options:
                    if activeHand.cards[0][0] in Hand.TENS:
                        key = '10s'
                    else:
                        key = str(activeHand.cards[0][0]) + 's'
                    move = Blackjack.SPLITCHART[key][upCardIndex]
                    #Split according to SPLITCHART.
                    if move.startswith('p'):
                        newHand = Hand(
                                activeHand.cards[1], 
                                self.shoe.deal()
                        )
                        activeHand.add_card(self.shoe.deal())
                        #Only allow stand or split after splitting aces.
                        if activeHand.cards[0][0] == 'A':
                        
                            activeHand.options = []
                            newHand.options = []
                            if (
                                   activeHand.cards[1][0] == 'A' and 
                                   len(player.hands) < 4
                            ):
                                activeHand.options.append('s')
                                activeHand.options.append('stand')
                                activeHand.options.append('p')
                                activeHand.options.append('split')
                            if (
                                    newHand.cards[1][0] == 'A' and 
                                    len(player.hands) < 4
                            ):
                                newHand.options.append('s')
                                newHand.options.append('stand')
                                newHand.options.append('p')
                                newHand.options.append('split')
                        player.hands[i] = activeHand
                        player.add_hand(newHand)
                        activeHand.discard(1)
                        if self.display:
                            firstHand = [c[0]+c[1] for c in activeHand.cards]
                            firstHand = ' '.join(firstHand)
                            secondHand = [c[0]+c[1] for c in newHand.cards]
                            secondHand = ' ' .join(secondHand)
                            print(f'{player.name} splits:')
                            print(f'{firstHand} total:', end=' ')
                            print(f'{activeHand.total}, {secondHand}', end=' ')
                            print(f'total: {newHand.total}')
                        continue
                key = activeHand.total
                if activeHand.soft:
                    move = Blackjack.SOFTCHART[key][upCardIndex]
                else:
                    move = Blackjack.CHART[key][upCardIndex]
                #Double according to either the hard or soft chart.
                if move.startswith('d'):
                    if 'd' in activeHand.options:
                        activeHand.double = 2
                        activeHand.add_card(self.shoe.deal())
                        active = False
                        if self.display:
                            cards = ' '.join([c[0]+c[1] for c in activeHand.cards])
                            print(f'{player.name} hits:', end=' ')
                            print(f'{cards} total: {activeHand.total}')
                    else:
                        move = move[1:]
                #Hit according to either the hard or soft chart.
                if move.startswith('h'):
                    activeHand.add_card(self.shoe.deal())
                    if self.display:
                        cards = ' '.join([c[0]+c[1] for c in activeHand.cards])
                        print(f'{player.name} hits:', end=' ')
                        print(f'{cards} total: {activeHand.total}')
                #Check if this Hand is over.
                if (
                        not activeHand.options or
                        activeHand.bust or
                        activeHand.total == 21 or
                        move.startswith('s')
                ):
                    if self.display:
                        if activeHand.bust:
                            print(f'{player.name} bust')
                        elif activeHand.bj:
                            print(f'{player.name} has Blackjack!')
                        else:
                            print(f'{player.name} stands')
                    active = False
            #Move to the next Hand.
            i += 1        

    def discard_hands(self) -> None:
        """Reinitialize hands for all players and the dealer."""
        for player in self.players:
            player.discard_hands()
        self.dealer.discard_hands()
        
    def check_ins(self) -> bool:
        """Check to see if any player wants to take insurance. 
        
        Return True if the dealer has blackjack and False otherwise.
        """
        dHand = self.dealer.hands[0]
        CHOICES = {'y', 'yes', 'n', 'no'}
        if dHand.cards[0][0] == 'A':
            for player in self.players:
                invalid = True
                while invalid:
                    response = input(
                            f'{player.name} ${player.bank}: ' +
                            'Do you want to take insurance?'
                    )
                    response = response.lower()
                    if response in CHOICES:
                        invalid = False
                        if response in {'y', 'yes'}:
                            if not dHand.bj:
                                player.bank -= player.bet / 2
                        """if response in {'n', 'no'}:
                            if dHand.bj and not player.hands[0].bj:
                                player.lose(player.bet)"""
                    else:
                        print('Please respond with (Y)es or (N)o')
            if dHand.bj:
                print(f'{self.dealer.name} has blackjack')
            else:
                print(f'{self.dealer.name} doesn\'t have blackjack')
        return dHand.bj
            
    def play_round(self) -> None:
        """Deal a round and prompt for input on how to play each player's Hand.
        """
        self.deal_round()
        self.show_hands()
        if not self.check_ins():
            for player in self.players:
                i = 0
                currentBets = 1
                bet = player.bet
                bank = player.bank
                print(f'{player.name}:')
                print(f'Bank: ${player.bank-player.bet} ', end='')
                print(f'Bet: ${player.bet}')
                #Allow a player to act on all hands.
                while i < len(player.hands):
                    active = True
                    activeHand = player.hands[i]
                    print(activeHand)
                    #Keep prompting until this hand is completed.
                    while active:
                        invalid = True
                        while invalid:
                            if activeHand.options:
                                if 'd' in activeHand.options:
                                    if bank < ((currentBets*bet) + bet):
                                        activeHand.options.remove('d')
                                        activeHand.options.remove('double')
                                if 'p' in activeHand.options:
                                    if (
                                            bank < ((currentBets*bet) + bet) or
                                            len(player.hands) >= 4
                                    ):
                                        activeHand.options.remove('p')
                                        activeHand.options.remove('split')
                                response = input(
                                        f'{activeHand.str_options()}? '
                                )
                                response = response.lower()
                                if response in activeHand.options:
                                    invalid = False
                                else:
                                    print('Invalid action')
                            else:
                                invalid = False
                                active = False
                                response = ''
                        if response in {'s', 'stand'}:
                            active = False
                        if response in {'h', 'hit'}:
                            activeHand.add_card(self.shoe.deal())
                            print(activeHand)
                            if activeHand.bj or activeHand.bust:
                                active = False
                        elif response in {'d', 'double'}:
                            activeHand.double = 2
                            activeHand.add_card(self.shoe.deal())
                            print(activeHand)
                            active = False
                        elif response in {'p', 'split'}:
                            newHand = Hand(
                                    activeHand.cards[1], 
                                    self.shoe.deal()
                            )
                            activeHand.discard(1)
                            activeHand.add_card(self.shoe.deal())
                            #Only allow stand or split after splitting aces.
                            if activeHand.cards[0][0] == 'A':
                                activeHand.options = []
                                newHand.options = []
                                if (
                                       activeHand.cards[1][0] == 'A' and 
                                       len(player.hands) < 4
                                ):
                                    activeHand.options.append('s')
                                    activeHand.options.append('stand')
                                    activeHand.options.append('p')
                                    activeHand.options.append('split')
                                if (
                                        newHand.cards[1][0] == 'A' and 
                                        len(player.hands) < 4
                                ):
                                    newHand.options.append('s')
                                    newHand.options.append('stand')
                                    newHand.options.append('p')
                                    newHand.options.append('split')
                            player.hands[i] = activeHand
                            player.add_hand(newHand)
                            print(activeHand)
                    i += 1
        print()
        self.play_dealer()
        self.calculate_winners()
        self.discard_hands()
        print()
        if self.shoe.shuffleFlag:
            print('Shuffling shoe')
            self.shoe.shuffle()
            
    def simulate_rounds(self, rounds: int = 100, 
            display: bool = False) -> None:
        """Deal a number of rounds and play all hands automatically. 
        
        Statistics are calculated and printed for each player. These statistics
        are for the entire session since the beginning of the program run. Use
        Player.reset_stats() to reset the statistics for a given Player.
        Keyword arguments:
        rounds  --  The number of rounds to play through. (100 default)
        display --  When this flag is set to True Hands and actions will be
                    printed to the screen. When the flag is set to False only
                    the resulting statistics will be printed. (False default)
        """
        self.display = display
        print(f'Simulating {rounds} hands...')
        for i in range(rounds):
            self.deal_round()
            if self.display:
                print('Dealer shows: {}{}'.format(*self.dealer.hands[0].cards[0]))
            for player in self.players:
                self.play_hand(player)
            self.play_dealer()
            self.calculate_winners()
            self.discard_hands()
            if self.shoe.shuffleFlag:
                self.shoe.shuffle()
            if self.display:
                print()
        for player in self.players:
            player.get_stats()
            print()
        self.display = True
        
    def add_player(
            self, name: str = None, bet: float = 10.0, bank: float = 100.0, 
            strat: Strategy = None
    ) -> None:
        """Add a player.
        
        Keyword arguments:
        name    --  The name of the new Player. If None is provided, the
                    Player's position will be used instead. (None default)
        bet     --  The first bet to be made by the Player. (10.0 default)
        bank    --  The amount of money the Player will have available. 
                    (100.0 default)
        strat   --  The betting Strategy to be used for this Player. If None is
                    provided, the bet will remain the same every round. 
                    (None default)
        """
        if not name:
            name = 'Player ' + str(len(self.players)+1)
        self.players.append(Player(name, bet, bank, self.minBet, strat))
        
    def remove_player(self, index: int = -1) -> None:
        """Remove a player.
        
        Keyword arguments:
        index    -- The index of the player to remove. This index is one less
                    than the table position and ranges from 0 to one fewer than
                    the number of players. If this is -1, the last player will 
                    be removed. (-1 default)
        """
        self.players.pop(index)
            
    def __str__(self) -> str:
        """Return a string representation of this game."""
        message = f'A {self.numberOfDecks}-deck game of blackjack with '
        message += f'{self.numberOfPlayers} players'
        return message
        
if __name__ == '__main__':
    """
    """
    game = True
    invalid = True
    menu = ['(P)lay a round','(S)imulate rounds', '(O)ptions', '(Q)uit']
    optionsMenu = [
            '(A)dd a player', 
            '(R)emove a player', 
            'Player (S)trategy', 
            '(M)ain Menu',
            '(Q)uit'
    ]
    responses = [
            'p', 'play', 'play a round', 
            's', 'simulate', 'simulate rounds',
            'o', 'options',
            'q', 'quit'
    ]
    strategyResponses = ['s', 'strategy', 'player strategy']
    menuResponses = ['m', 'main', 'menu', 'b', 'back']
    optionResponses = [
            'a', 'add', 'add a player', 
            'r', 'remove', 'remove a player',
            *strategyResponses,
            *menuResponses,
            'q', 'quit'
    ]
    print('Welcome to Dan\'s Blackjack simulator!')
    while invalid:
        players = input(
                'How many players would you like to start the game with? ' + 
                '(1-8): '
        )
        try:
            if int(players) > 8:
                print('A maximum of 8 players are allowed.')
            else:
                invalid = False
        except ValueError as e:
            print('Please enter a int 1-8.')
        else:
            myBJ = Blackjack(6,int(players))
    while game:
        invalid = True
        while invalid:
            print('Main Menu:', end=' ')
            response = input(', '.join(menu) + '? ')
            repsonse = response.lower()
            if response not in responses:
                print('Invalid command.')
            else:
                invalid = False
                if response.startswith('p'):
                    myBJ.play_round()
                elif response.startswith('s'):
                    display = 'How many rounds would you like to simulate? '
                    rounds = int(input(display))
                    myBJ.simulate_rounds(rounds)
                elif response.startswith('o'):
                    option = True
                    while option:
                        print('Options:', end=' ')
                        response = input(', '.join(optionsMenu) + '? ')
                        if response not in optionResponses:
                            print('Invalid command.')
                        else:
                            if response in strategyResponses:
                                strat = True
                                while strat:
                                    for player in myBJ.players:
                                        print(f'{player.name}\'s strategy:')
                                        print(f'{player.strat}\n')
                                    display = ('For which player position ' +
                                            'would you like to create a ' +
                                            'strategy? ')
                                    response = input(display)
                                    try:
                                        position = int(response)
                                        if position > len(myBJ.players):
                                            raise ValueError
                                    except ValueError as e:
                                        print('Invalid player position.')
                                    else:
                                        strat = False
                                        myBJ.players[position-1].create_strat()
                            elif response.startswith('a'):
                                name = input(
                                        'What is the name of this player? '
                                )
                                myBJ.add_player(name)
                            elif response.startswith('r'):
                                invalid = True
                                while invalid:
                                    players = len(myBJ.players)
                                    position = input(
                                            'Enter the position of the ' +
                                            'player that you would like to ' +
                                            'remove: '
                                    )
                                    try:
                                        position = int(position) - 1
                                    except ValueError:
                                        print(
                                                'Please enter a position ' +
                                                f'1-{players}'
                                        )
                                    else:
                                        if position > players or position < 0:
                                            print(
                                                    'Please enter a postion ' +
                                                    f'1-{players}'
                                            )
                                        else:
                                            myBJ.remove_player(position)
                                            invalid = False
                            elif response in menuResponses:
                                option = False
                            elif response.startswith('q'):
                                option = False
                if response.startswith('q'):
                    game = False