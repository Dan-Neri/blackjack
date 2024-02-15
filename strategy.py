class _betIterator:
    """This class is an iterator used to easily determine the next bet when
    using a progressive betting strategy.
    """
    def __init__(
            self, initial: float, increment: float|str, maxBet: int
    ) -> None:
        """Initialize the iterable object.
        
        Keyword arguments:
        initial     --  The initial value of this iterator.
        increment   --  The amount to increase or decrease the bet once the
                        pattern has been exhausted.
        maxBet      --  The maximum allowed bet for this iterator.
        """
        try:
            if type(increment) not in [int, float, str]:
                raise ValueError('Invalid Increment type')
            if type(increment) == str and not self.is_multiplier(increment):
                raise ValueError('Invalid Increment string')
            if float(initial) < 1:
                raise ValueError('Initial value must be at least 1 unit')
            if int(maxBet) < initial:
                raise ValueError('Max bet must be larger than the initial bet')
        except ValueError as e:
            print(f'BetIterator declaration error: {e}')
            raise
        except Exception as e:
            print(f'BetIterator declaration error: {e}')
            raise
        else:
            self.increment = increment
            self.pattern = [float(initial)]
            self.maxBet = int(maxBet)

    def __iter__(self) -> None:
        """Initialize the iterator."""
        self.count = 0
        self.bet = self.pattern[0]
        return self

    def __next__(self) -> float:
        """Return the next value of the iterator.
        
        The values of the iterator will start with the elements in the pattern.
        Once the pattern is exhausted, the bet will change based on the
        increment.
        """
        if self.count >= len(self.pattern):
            if self.is_multiplier(self.increment):
                self.bet *= float(self.increment.strip('*'))
            else:
                self.bet += self.increment
            if self.bet < 1:
                self.bet = 1.0
                self.count = 0
                return self.bet
            if self.bet > self.maxBet:
                self.bet = float(self.maxBet)
        else:
            self.bet = self.pattern[self.count]
        self.count += 1
        return self.bet
        
    def set_count(self, count: int = 0) -> None:
        """Set the count.
        
        The count is an indication of how many times next() has been called
        on this iterator.
        """
        try:
            self.count = int(count)
        except ValueError:
            print('Cannot set the count. Please use an int amount.')
            
    def set_bet(self, bet: float) -> None:
        """Set the current bet."""
        try:
            self.bet = float(bet)
        except ValueError:
            print('Cannot set the bet. Please use a float amount.')
    
    def set_max(self, bet: int) -> None:
        """Set the maximum allowed bet."""
        try:
            self.maxBet = int(bet)
        except ValueError:
            print('Cannot set the max bet. Please use an int amount')
    
    def set_pattern(self, pattern: list[float | str]) -> None:
        """Set the initial pattern of bets."""
        backup = self.pattern
        self.pattern = []
        for i in pattern:
            if self.add_step(i) == -1:
                print('Cannot set pattern. Usage: list[bet]')
                print('Bet must be either a float or a str in the', end=' ')
                print('form \'*multiplier\'')
                self.pattern == backup
                return
            
    def set_increment(self, increment: float | str = 0.0) -> None:
        """Set the final increment value.
        
        Positive values will increase the bet once the values in the pattern
        have been exhausted. Negative values will decrease the bet. If
        increment begins with a '*', the previous value will be multiplied 
        instead of added.
        """
        try:
            if type(increment) not in [int, float, str]:
                raise ValueError('Invalid Increment type')
            elif type(increment) == str and not self.is_multiplier(increment):
                raise ValueError('Invalid Increment string')
            else:
                if type(increment) == str:
                    self.increment = increment
                else:
                    self.increment = float(increment)
        except ValueError as e:
            print(f'Cannot set increment: {e}.')
            print('Please use a a float or a str in the form \'*multiplier\'')
            

        self.count = 0
        
    def is_multiplier(self, step: float | str) -> bool:
        """Check if step is a multiplier and return as a bool."""
        if type(step) == str and step.startswith('*'):
            return True
        else:
            return False
            
    def add_step(self, step: float | str) -> int:
        """Add a new step to the end of the bet pattern."""
        try:
            if self.is_multiplier(step):
                step = self.pattern[-1] * float(value.strip('*'))
            self.pattern.append(float(step))
        except ValueError:
            print(f'Invalid step: {step}')
            return -1
        else:
            return 0
    
    def __str__(self):
        """Return a string representation of this _betIterator"""
        display = f'{self.pattern} '
        if type(self.increment) == float:
            display += f'{self.increment:+}'
        else:
            display += str(self.increment)
        return display


class Strategy:
    """This class represents a complete progressive betting strategy. It
    utilizes two instances of _betIterator to give it the flexibility to handle
    multiple types of winning and losing progressions. It also tracks the
    total number of hands won/lost as well as the longest win/lose streak.
    """
    def __init__(
            self, initialWin: float, incrementWin: float | str,
            initialLose: float, incrementLose: float | str, maxBet: int
    ) -> None:
        """Create an iterable object and an iterator for both win and lose.
        
        Keyword arguments:
        initialWin      --  The first value to bet after a win.
        incrementWin    --  The amount to increment the bet upon a win once the 
                            pattern has been exhausted. This can be either a
                            set amount to increase/decrease the bet or a
                            multiplier in the form '*multiplier'.
        initialLose     --  The first value to bet after a loss.
        incrementLose   --  The amount to increment the bet upon a loss once
                            the pattern has been exhausted.
        maxBet          --  The maximum bet allowed for this Strategy.
        """
        self.winStreak, self.maxWins, self.winTotal = 0, 0, 0
        self.loseStreak, self.maxLoses, self.loseTotal = 0, 0, 0
        self.incrementWin = incrementWin
        self.incrementLose = incrementLose
        self.maxBet = maxBet
        self.winStrat = _betIterator(initialWin, incrementWin, maxBet)
        self.winSeq = iter(self.winStrat)
        self.loseStrat = _betIterator(initialLose, incrementLose, maxBet)
        self.loseSeq = iter(self.loseStrat)

    def win(self) -> float:
        """Record a win and return the next value in the win iterator."""
        self.winTotal += 1
        self.loseStreak = 0
        self.winStreak += 1
        if self.winStreak > self.maxWins:
            self.maxWins = self.winStreak
        if (((type(self.incrementWin) in {float, int} and
                self.incrementWin < 0) or
                (type(self.incrementLose) in {float, int} and
                self.incrementLose < 0)) and
                self.winSeq.count == 0):
            self.winSeq.set_count(self.loseSeq.count)
            self.winSeq.set_bet(self.loseSeq.bet)
        if ((type(self.incrementWin) in {float, int} and
                self.incrementWin <= 0) or
                (type(self.incrementLose) in {float, int} and
                self.incrementLose <= 0)):
            self.loseSeq = iter(self.loseStrat)
        return next(self.winSeq)

    def lose(self) -> float:
        """Record a loss and return the next value in the lose iterator."""
        self.loseTotal += 1
        self.winStreak = 0
        self.loseStreak += 1
        if self.loseStreak > self.maxLoses:
            self.maxLoses = self.loseStreak
        if (((type(self.incrementWin) in {float, int} and
                self.incrementWin < 0) or
                (type(self.incrementLose) in {float, int} and
                self.incrementLose < 0)) and
                self.loseSeq.count == 0):
            self.loseSeq.set_count(self.winSeq.count)
            self.loseSeq.set_bet(self.winSeq.bet)
        if ((type(self.incrementLose) in {float, int} and
                self.incrementLose <= 0) or
                (type(self.incrementWin) in {float, int} and
                self.incrementWin <= 0)):
            self.winSeq = iter(self.winStrat)
        return next(self.loseSeq)

    def add_win(self, step: float | str) -> None:
        """Add a step to the end of the bet pattern for the win iterable."""
        self.winStrat.add_step(step)

    def add_lose(self, step: float | str) -> None:
        """Add step to the end of the bet pattern for the lose iterable."""
        self.loseStrat.add_step(step)

    def set_max(self, bet: int) -> None:
        """Set the maximum allowed bet for this Strategy."""
        if type(bet) != int:
            print('Max bet must be an integer')
            return
        else:
            self.winStrat.set_max(bet)
            self.loseStrat.set_max(bet)
            self.maxBet = bet
            
    def __str__(self) -> str:
        """Return a string representation of this Strategy."""
        display = (
                f'win: {self.winStrat}\n' +
                f'lose: {self.loseStrat}\n' +
                f'max: {self.maxBet}'
        )
        return display


if __name__ == '__main__':
    myStrat = Strategy(2, 2, 1, -1, 1000)
    myStrat.add_win(4)
    myStrat.add_lose(2)
    print(myStrat)
    myStrat.set_max(500)
    myStrat.lose()
    myStrat.win()
    print(myStrat)