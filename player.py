from strategy import Strategy
from hand import Hand

import textwrap

class Player:
    """This class represents a blackjack player."""
    
    def __init__(
            self, name: str = 'Player', bet: float = 10.0, bank: float = 100.0,
            minBet: int = 10, strat: Strategy = None
    ):
        """Initialize a new Player with one empty Hand.
        
        A player can have multiple Hands which are stored in the hands list.
        debt indicates the total amount the player has put onto the table, into
        their bank. The property winnings is a calulation of the total amount
        won/lost by the player. maxWinnings and minWinnings keep track of the
        highest and lowest value of winnings respectively.
        
        Keyword arguments:
        name    --  The name of the player. ('Player' default)
        bet     --  The initial value of the player's bet. (10.0 default)
        bank    --  The amount of money the player has on the table. 
                    (100.0 default)
        minBet  --  The lowest bet amount allowed for the player. (10 default)
        strat   --  The betting Strategy for the player. If None is provided,
                    the strategy is set to keep the bet the same after either a
                    win or a loss with a maxBet of 1000. (None default)
        """
        self.name = str(name)
        self.bank = float(bank)
        self.debt = float(bank)
        self.bet = float(bet)
        self.hands = [Hand()]
        self.minBet = minBet
        self.maxWinnings = 0
        self.minWinnings = 0
        if strat:
            self.strat = strat
        else:
            self.strat = Strategy(1, 0, 1, 0, 1000)
        if self.bank < self.minBet:
            raise ValueError('Player\'s bank must be at least their minBet.')
        if self.minBet > bet > self.strat.maxBet:
            raise ValueError(
                    'Player\'s bet must be between their minBet and maxBet'
            )
    
    @property
    def winnings(self):
        """The total amount won by the player."""
        return self.bank - self.debt
        
    def set_bet(self, bet: float) -> None:
        """Update the Player's bet.
        
        Keyword arguments:
        bet --  The amount to change the bet to. This value must be between 
                minBet and maxBet specified for the Player.
        """
        try:
            bet = float(bet)
        except ValueError as e:
            print('Cannot set bet. Please use a float amount.')
        else:
            if bet < self.minBet:
                print(f'Cannot set bet. Bet must be at least ${self.minBet}')
            elif bet > self.strat.maxBet:
                print('Cannot set bet. Bet cannot be greater than', end=' ')
                print(f'${self.maxBet}')
            else:
                self.bet = bet
            
    def add_hand(self, hand: Hand = Hand()) -> None:
        """Add a new Hand to the end of the list of the Player's Hands."""
        self.hands.append(hand)
    
    def discard_hands(self) -> None:
        """Set the Player's list of Hands to a single empty Hand."""
        self.hands = [Hand()]
        
    def win(self, amount: int | None = None) -> None:
        """Record a win. Update the Player's bank and bet accordingly."""
        if amount:
            self.bank += amount
        else:
            self.bank += self.bet
        self.bet = self.minBet * self.strat.win()
        if self.winnings > self.maxWinnings:
            self.maxWinnings = self.winnings
        if self.bank < self.minBet:
            self.rebuy()
        if self.bank < self.bet:
            self.bet = self.bank
        
    def lose(self, amount: int | None = None) -> None:
        """Record a loss. Update the Player's bank and bet accordingly."""
        if amount:
            self.bank -= amount
        else:
            self.bank -= self.bet
        self.bet = self.minBet * self.strat.lose()
        if self.winnings < self.minWinnings:
            self.minWinnings = self.winnings
        if self.bank < self.minBet:
            self.rebuy()
        if self.bank < self.bet:
            self.bet = self.bank
        
    def rebuy(self, amount: float = 100.0):
        """Increase the Player's bank and debt.
        
        Keyword arguments:
        amount  --  The amount to add to the Player's bank.
        """
        try:
            if self.bank+float(amount) < self.minBet:
                print(f'Must rebuy at least ${self.minBet-self.bank}')
            else:
                self.bank += float(amount)
                self.debt += float(amount)
                if self.winnings < self.minWinnings:
                    self.minWinnings = self.winnings
        except ValueError as e:
            print('Cannot rebuy. Please use a float amount.')
        
    def create_strat(self) -> None:
        """Prompt for keyboard input to create a new Strategy for the Player.
        
        initialWin and initialLose are the start of the win and lose bet
        progession respectively. That is to say:
        intialWin = self.winStrat.pattern[0]. The win pattern is followed every
        time a hand is won and the lose pattern every time a hand is lost. Once
        either pattern has been exhausted, the final value will be incremented
        by winIncrement or loseIncrement so that the next bet value can be
        determined. If the maxBet is exceeded the bet will instead be set to
        maxBet.
        """
        loop = True
        responses = {'win', 'lose', 'no', 'w', 'l', 'n', 'exit', 'e', 'stop'}
        print('Let me help you create a strategy.')
        print('Please enter all values as multiples of the minimum bet.') 
        display = (
                'For example, if you are playing at a table with a $10 ' +
                'minimum and want to create this strategy: First bet $10, ' + 
                'increase your bet by $5 every time you win a hand, and ' +
                'reset the bet back to $10 when you lose a hand.\nEnter 1.5 ' +
                'for the bet amount after your first win, 1 for the bet ' +
                'after your first loss, 0.5 for the amount to increase your ' +
                'bet after a win, and 0 for the amount to increase after a ' +
                'loss.'
        )
        print(textwrap.fill(display, 79))
        initialWin = input('What would you like the bet to be after your ' +
                'first win? ')
        initialLose = input('What would you like the bet to be after your ' +
                'first loss? ')
        incrementWin = input('How much would you like the bet to increase ' +
                'after each subsequent win? ')
        display = ()
        incrementLose = input('How much would you like the bet to increase ' +
                'after each subsequent loss? ')
        maxBet = input('What would you like your max bet to be? ')
        try:
            initialWin = float(initialWin)
            initialLose = float(initialLose)
            if not incrementWin.startswith('*'):
                incrementWin = float(incrementWin)
            if not incrementLose.startswith('*'):
                incrementLose = float(incrementLose)
            maxBet = int(maxBet)
        except ValueError as e:
            print('Invalid strategy values')
            return
        self.strat = Strategy(initialWin, incrementWin, initialLose, 
                incrementLose, maxBet)
        while loop:
            print('Would you like to add any other steps to your win or lose' +
                    ' progression?')
            response = input('(Enter (w)in, (l)ose or (n)o)) ')
            response = response.lower()
            if response not in responses:
                print('Invalid response')
                continue
            elif response in {'win', 'w'}:
                step = input('Enter the amount you would like to bet after ' +
                        f'{len(self.strat.winStrat.pattern)+1} wins ')
                self.strat.add_win(step)
            elif response in {'lose', 'l'}:
                step = input('Enter the amount you would like to bet after ' +
                        f'{len(self.strat.loseStrat.pattern)+1} losses ')
                self.strat.add_lose(step)
            elif response in {'no', 'n', 'exit', 'e', 'stop'}:
                print(f'{self.name}\'s strategy has been set to:')
                print(self.strat)
                loop = False
                
    def get_stats(self) -> None:
        """Print various stats for the given player."""
        print(f'{self.name} Strategy:')
        print(self.strat)
        print('-----Stats-----')
        print(f'Total winnnigs: {self.winnings}')
        print(f'Total hands won: {self.strat.winTotal}')
        print(f'Max win streak: {self.strat.maxWins}')
        print(f'Max balance: {self.maxWinnings}')
        print(f'Total hands lost: {self.strat.loseTotal}')
        print(f'Max lose streak: {self.strat.maxLoses}')
        print(f'Min balance: {self.minWinnings}')
    
    def reset_stats(self):
        """Resets all stats for the Player."""
        self.strat.winTotal, self.strat.maxWins, self.maxWinnings, = 0, 0, 0
        self.strat.loseTotal, self.strat.maxLoses, self.minWinninngs = 0, 0, 0
        
    def __str__(self) -> str:
        """Return a string representation of this Player."""
        return f'{self.name} - Bank: {self.bank} Bet: {self.bet}'


if __name__ == '__main__':
    player1 = Player('Player1', 30, 500, 10, Strategy(2, -1, 4, 1, 500))
    player2 = Player('Player2', strat=Strategy(1.5, 0.5, 1, -0.5, 1000))
    print(f'Player: {player1}\nStrategy:\n{player1.strat}')
    for i in range(6):
        print(player1.bet, end=', ')
        player1.win()
    print(f'{player1.name}: {player1.bank}')
    for i in range(3):
        print(player1.bet, end=', ')
        player1.lose()
    print(f'{player1.name}: {player1.bank}\n')  
    print(f'Player: {player2}\nStrategy:\n{player2.strat}')
    for i in range(6):
        print(player2.bet, end=', ')
        player2.win()
    print(f'{player2.name}: {player2.bank}')
    for i in range(3):
        print(player2.bet, end=', ')
        player2.lose()
    print(f'{player2.name}: {player2.bank}')