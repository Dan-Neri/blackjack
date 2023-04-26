"""This simulator will play out a certain number of blackjack hands according
to basic blackjack strategy and give stats on the number of hands won/lost as
well as the total amount of money won/lost. Useful for testing out different
betting strategies"""
import itertools, random

import cards

class blackjack(cards.Cards):
    """This class holds different methods specific to blackjack and inherits
    from Cards"""
    
    def __init__(self, players=1):
        """Overrides the original constructor from Cards and calls the
        constructor defined below in blackjack instead"""
        self.__init__(players, 6, 1)
        
    def __init__(self, number_of_players=1, bet=10, number_of_decks=6, b=1):
        """Initializes a new dealer shoe with the specified number of players
        and decks. The max number of players is 6. Note that the number of 
        hands will actually be one more than the number of players to account 
        for the dealer's hand. A random shuffle_card is determined which will 
        trigger shuffle_flag indicating it is time to shuffle the shoe."""
        self.decks = number_of_decks
        self.min_bet = bet;
        self.burn = b
        self.deck = self.new_shoe(number_of_decks)
        self.players = []
        self.shuffle_card = random.randint(52, 104)
        self.shuffle_card = False
        self.number_of_players = number_of_players
        self.hand_count = number_of_players + 1
        
        if number_of_players > 6:
            print("The maximum number of players in this game is 6")
            number_of_players = 6
        for p in range(number_of_players + 1):
            if p == number_of_players:
                self.players.insert(p, self.create_player("Dealer", bet))
            else:
                self.players.insert(
                    p, 
                    self.create_player(f"Player {p + 1}", bet)
                )
            self.players[p]['original_position'] = p       
        print(f"A new game of blackjack with {number_of_players} player(s) has"
            + " been started")
        
    def create_player(self, n = 'Player', bet_amount=10, bank=100,):
        """Returns a dictionary representing a new player with the specified 
        name, initial bankroll, bet amount, an empty hand, and an empty hand 
        result"""
        return {
            'name': n, 
            'bankroll': bank, 
            'bet': bet_amount, 
            'hand': [], 
            'hand_result': {'total':None, 'soft':False, 'bust':False, 'bj':False},
            'double': False,
            'split_count': 0,
            'split_hand': False
        }
        
    def new_shoe(self, decks=6):
        """Returns a list representing a dealer shoe containing the specified 
        cards from the specified number of decks"""
        temp_deck = []

        for i in range(decks):
            temp_deck = itertools.chain(temp_deck, self.new_deck())
        
        return list(temp_deck)
        
    def show_hands(self):
        """Prints each player's current hand along with the total. Only the 
        first card in the dealer's hand is shown"""
        for i in range(self.hand_count):
            player = self.players[i]
            if player['hand']:
                print(f"{player['name']}:", end=' ')
                
                #Hides the dealer's second card
                if i == self.hand_count - 1:
                    print("{:>2}{}".format(*player['hand'][0]), end=' ')
                    print("{:>2}{}".format(*"XX"))
                    self.calculate_total(i)
                else:
                    #Displays both cards in the other players' hands
                    for card in player['hand']:
                        print("{:>2}{}".format(*card), end=' ')
                    self.calculate_total(i)
                
                    #Displays the hand total and the soft, bust, or blackjack
                    #flag if flipped
                    print(
                        f"Total: {player['hand_result']['total']} " +
                        f"{'Soft' if player['hand_result']['soft'] else ''} " + 
                        f"{'Bust' if player['hand_result']['bust'] else ''} " +
                        f"{'Blackjack!' if player['hand_result']['bj'] else ''}"
                    )
            else:
                print("Empty")
    
    def show_hand(self, position=0):
        """Prints the specified player's hand along with the total"""
        player = self.players[position]
        if player['hand']:
            print(f"{player['name']}:", end=' ')
            
            #Displays each card in the players hand
            for card in player['hand']:
                print("{:>2}{}".format(*card), end=' ')
            
            self.calculate_total(position)
                
            #Displays the hand total and the soft or bust flag if flipped
            print(
                f"Total: {player['hand_result']['total']} " +
                f"{'Soft' if player['hand_result']['soft'] else ''} " + 
                f"{'Bust' if player['hand_result']['bust'] else ''} " +
                f"{'Blackjack!' if player['hand_result']['bj'] else ''}"
            )
        else:
            print("Empty")
                
    def shuffle_shoe(self):
        """Discards any current hands, shuffles the shoe, and burns the 
        required number of cards"""
        self.deck = self.new_shoe(self.decks)
        random.shuffle(self.deck)
        self.discard_hands()
        self.shuffle_card = random.randint(52, 104)
        self.shuffle_flag = False
        for i in range(self.burn):
            self.deck.pop()
        print("The shoe has been shuffled")
        
    def shuffle_deck(self):
        """Overrides the original shuffle_deck method from cards to shuffle an
        entire shoe instead"""
        self.shuffle_shoe()
        
    def deal(self, number=2):
        """Overrides the original deal method from cards to check if the
        shuffle_card has been dealt or not"""
        
        #Checks if there are enough cards in the deck
        if number * self.hand_count > len(self.deck):
            print(
                f"There are not enough cards left in the deck to deal {number}" 
                + " card(s) to each player. The hand must be restarted.")
            self.shuffle_shoe()
        else:
            print(f"Dealing {number} card(s) to each player")
            
            #Checks if the shuffle card has been dealt
            if (
                    len(self.deck) - (number * self.hand_count) <= 
                    self.shuffle_card
            ):
                print(f"The shuffle card has been dealt. The shoe will be "
                    + "shuffled after this hand")
                self.shuffle_flag = True
            for n in range(number):
                for player in self.players:
                    player['hand'].append(self.deck.pop())
                    
    def discard_hands(self):
        """Discards all players hands"""
        print("Discarding all players hands")
        for player in self.players:
            player['hand'] = []
            player['hand_result'] = {
                'total':None,
                'soft':False,
                'bust':False,
                'bj':False}
            
    def set_players(self, number=1, bet=10):
        """sets the number of players in the game. The current players' and
        dealer's hands will be discarded but the shoe will remain the same"""
        self.players = []
        for p in range(number + 1):
            if p == self.hand_count - 1:
                self.players.insert(p, self.create_player("Dealer"))
            else:
                self.players.insert(
                    p, 
                    self.create_player(f"Player {p + 1}"), 
                    bet
                )
        print(f"The number of players has been set to {players}")

    def hit(self, position=0):
        """Adds a single card to the specified players hand. Calculates the
        total and returns the result"""
        player = self.players[position]
        
        #Checks if the next card is the shuffle card
        if self.shuffle_card > len(self.deck) and self.shuffle_flag == False:
            self.shuffle_flag = True
            print("The shuffle card has been dealt. The shoe will be shuffled"
                + "after this hand")
         
        player['hand'].append(self.deck.pop())
        if player['double'] == player['bet']:
            print(f"{player['name']} doubles")
        elif player['double'] > 0:
            print(f"{player['name']} doubles for less")
        else:
            print(f"{player['name']} hits") 
        self.calculate_total(position)
        self.show_hand(position)
        
    def split(self, position):
        """Splits the hand at the given position creating a temp player which
        is added to the hand to represent the new position. All temp players
        will be removed from the hand after the calculate_winners method is
        called"""
        player = self.players[position]
        original_position = player['original_position']
        original_player = self.players[original_position]
        
        
        #Store the players current cards
        card1 = player['hand'][0]
        card2 = player['hand'][1]
        
        #Add a new card from the top of the deck to the player's first hand and
        #calculate their new total
        player['hand'][1] = self.deck.pop()
        self.calculate_total(position)
        self.show_hand(position)
        
        original_player['split_count'] += 1
        
        #determine the temp player's name
        if original_player['split_count'] == 1:
            name = f"{original_player['name']}'s second hand"
        elif original_player['split_count'] == 2:
            name = f"{original_player['name']}'s third hand"
        elif original_player['split_count'] == 3:
            name = f"{original_player['name']}'s fourth hand"
            
        #Add a temp player to the list of players to handle the player's second
        #hand and note the original players hand
        self.players.insert(position+1,self.create_player(name, player['bet']))
        temp_player = self.players[position + 1]
        temp_player['original_position'] = original_position
        
        #This flag denotes that this player is temporary and will be removed
        #after the calculate winners method is called
        temp_player['split_hand'] = True
        
        #Add the correct cards to the player's second hand and calculate its
        #total
        temp_player['hand'].append(card2)
        temp_player['hand'].append(self.deck.pop())
        self.calculate_total(position+1)
        self.show_hand(position+1)
        
        #update the hand count
        self.hand_count += 1
        
    def calculate_total(self, position=0):
        """Analyzes the given players hand and creates a list containing the
        the hand total, a flag indicating if the hand is soft, one indicating
        if the player has bust, and one indicating if they have a blackjack. 
        It then stores this list in the player's hand_result attribute"""
        player = self.players[position]
        total = 0
        soft_flag = False
        bust_flag = False
        bj_flag = False
        
        for card in player['hand']:
            if type(card[0]) == int:
                total += card[0]
            elif card[0] == 'A':
                if total + 11 > 21:
                    total += 1
                else:
                    total += 11
                    soft_flag = True
            else:
                total += 10
                
            if total == 21 and len(player['hand']) == 2:
                    bj_flag = True
                    soft_flag = False
            elif total > 21:
                if soft_flag:
                    total -= 10
                    soft_flag = False
                else:
                    bust_flag = True
        
        result = {
            'total':total, 
            'soft':soft_flag, 
            'bust':bust_flag, 
            'bj':bj_flag
            }
        player['hand_result'] = result
        
    def calculate_winners(self):
        """Compares each player's hand to the dealer's hand to determine who
        wins. Then updates that player's bankroll accordingly with their bet 
        amount"""
        dealer_hand = self.players[-1]['hand_result']
        i = 0
        while i < self.hand_count-1:
            player = self.players[i]
            original_player = self.players[player['original_position']]
            hand_result = player['hand_result']
            
            if hand_result['bust']:
                original_player['bankroll'] -= player['bet'] + player['double']
                print(f"{player['name']} busted.", end=' ')
            elif hand_result['total'] == dealer_hand['total']:
                print(f"{player['name']} pushed.", end=' ')
            elif hand_result['bj']:
                original_player['bankroll'] += player['bet']*1.5
                print(f"{player['name']} has blackjack!", end=' ')
            elif dealer_hand['bust'] or hand_result['total'] > dealer_hand['total']:
                original_player['bankroll'] += player['bet'] + player['double']
                print(f"{player['name']} won!", end=' ')
            elif hand_result['total'] < dealer_hand['total']:
                original_player['bankroll'] -= player['bet'] + player['double']
                print(f"{player['name']} lost.", end=' ')
            print("You have ${:.2f}".format(original_player['bankroll']))
            player['double'] = 0
            if player['split_hand']:
                original_player['split_count'] -= 1
                del self.players[i]
                self.hand_count -= 1
                i -= 1
            i += 1
        print("\r")
            
    def play_dealer_hand(self):
        """Simulates the dealer playing their hand. The dealer hits on all hand
        values less than 17. Hits on soft 17 and stands on all hands 17 or
        higher"""
        dealer = self.players[-1]
        active = False
        #check to see if all players have blackjack or bust
        for i in range(self.hand_count-1):
            if (
                    not self.players[i]['hand_result']['bj'] and 
                    not self.players[i]['hand_result']['bust']
            ):
                active = True
        if active == True:
            #checks to see if the dealer needs to hit
            if (
                dealer['hand_result']['total'] < 17 or 
                (dealer['hand_result']['total'] == 17 and 
                    dealer['hand_result']['soft']
                )
            ):
                active = True
            else:
                active = False
            while active:
                self.hit(self.hand_count-1)
                if dealer['hand_result']['total'] > 17:
                    active = False
                elif (
                        dealer['hand_result']['total'] == 17 and 
                        not dealer['hand_result']['soft']
                ):
                    active = False
            if dealer['hand_result']['bust']:
                print(f"{dealer['name']} Busts")
            else:
                print(f"{dealer['name']} stands")

    def set_bet(self, position, amount):
        """Changes the bet amount of the specified player"""
        if position > self.number_of_players - 1:
            print("The specified position is not valid")
        else:
            player = self.players[position]
        
        if amount > player['bankroll']:
            print(f"{player['name']} does not have enough to bet {amount}")
        else:
            player['bet'] = amount
            print(f"{player['name']}'s bet is now {player['bet']}")
        
    def play_round(self):
        """This method simulates playing one 'round' of blackjack"""
        self.discard_hands()
        self.deal()
        self.show_hands()
        dealer = self.players[-1]
            
        #Check if the dealer is showing an ace and calculate insurance
        if dealer['hand'][0][0] == 'A':
            for i in range(self.hand_count-1):
                player = self.players[i]
                ins = input(f"{player['name']} would you like " +
                    "insurance? ")
                if ins == 'y' or ins == 'yes':
                    player['insurance'] = True
                    if dealer['hand_result']['total'] != 21:
                        player['bankroll'] -= player['bet']/2
                    else:
                        player['bankroll'] += player['bet']
                else:
                    player['insurance'] = False
            if dealer['hand_result']['total'] != 21:
                print(f"{dealer['name']} does not have blackjack")
        if dealer['hand_result']['total'] == 21:
            print(f"{dealer['name']} has blackjack")
        else:   
            i = 0
            #allow each player to play their hand
            while i < self.hand_count-1:
                player = self.players[i]
                active = True
                
                #Check if the player has blackjack
                if self.players[i]['hand_result']['bj']:
                    active = False
                #loop while this player's hand is active
                while active:
                    #evaluates value of face cards and aces in a player's hand
                    if  type(self.players[i]['hand'][0][0]) == int:
                        card_one_value = self.players[i]['hand'][0][0]
                    elif self.players[i]['hand'][0][0] == 'A':
                        card_one_value = 1
                    else:
                        card_one_value = 10
                    if  type(self.players[i]['hand'][1][0]) == int:
                        card_two_value = self.players[i]['hand'][1][0]
                    elif self.players[i]['hand'][1][0] == 'A':
                        card_two_value = 1
                    else:
                        card_two_value = 10
                    #Checks if the player is able to split or double
                    if (
                            len(self.players[i]['hand'])==2 and
                            self.players[player['original_position']]['split_count']<4 and
                            card_one_value==card_two_value
                    ):
                        valid = False
                        while not(valid):
                            matches = [
                                's', 
                                'stand', 
                                'h', 
                                'hit', 
                                'sp', 
                                'split', 
                                'd', 
                                'double']
                            response = input(f"{self.players[i]['name']} "
                                + "(s)tand, (h)it?, (sp)lit or (d)ouble? ")
                            if any(x in response for x in matches):
                                valid = True
                        #Checks if the player wants to split
                        if response == 'split' or response == 'sp':
                            self.split(i)
                    #Checks if the player is able to double. This is allowed
                    #for any value of the first two cards
                    elif (len(self.players[i]['hand'])==2):
                        valid = False
                        while not(valid):
                            matches = ['s', 'stand', 'h', 'hit', 'd', 'double']
                            response = input(f"{self.players[i]['name']} "
                                + "(s)tand, (h)it?, or (d)ouble? ")
                            if any(x in response for x in matches):
                                valid = True
                    #Menu for players who can only stand or hit
                    else:
                        valid = False
                        while not(valid):
                            matches = ['s', 'stand', 'h', 'hit']
                            response = input(f"{player['name']} " +
                                "(s)tand or (h)it? ")
                            if any (x in response for x in matches):
                                valid = True
                    #Checks if the player has blackjack
                    if player['hand_result']['bj']:
                        active = False
                        continue
                        
                    #checks if the player wants to double
                    if response == 'double' or response == 'd':
                        if player['bankroll'] < player['bet'] * 2:
                            confirm = input(
                                "You do not have enough funds to double." +
                                " Would you like to double for less? "
                            )
                            if confirm == 'yes' or confirm == 'y':
                                player['double'] = player['bankroll']
                                active = False
                            else:
                                response = input("Would you like to (s)tand " +
                                    "or (h)it? ")
                        elif (
                                player['hand_result']['total'] > 11 and
                                player['hand_result']['soft'] == False
                        ):
                            confirm = input("You have " +
                                f"{player['hand_result']['total']}. Are " +
                                "you sure you want to double? ")
                            if confirm == 'yes' or confirm == 'y':
                                player['double'] = player['bet']
                                active = False
                            else:
                                response = input("Would you like to (s)tand " +
                                    "or (h)it? ")
                        else:
                            player['double'] = player['bet']
                            active = False
                    if (
                            response == 'hit' or 
                            response == 'h' or 
                            response == 'double' or 
                            response == 'd'
                    ):
                        self.hit(i)
                        
                        #checks if the player has bust
                        if player['hand_result']['bust']:
                            active = False
                            
                        #Checks if the player has 21
                        if player['hand_result']['total'] == 21:
                            print("21!!")
                            active = False
                    else:
                        print(f"{player['name']} stands")
                        active = False
                i += 1
        self.show_hand(self.hand_count-1)
        self.play_dealer_hand()
        self.calculate_winners()
        
        #if the shuffle card has been dealt, shuffle the shoe, otherwise just
        #discard the current hand
        if self.shuffle_flag:
            self.shuffle_shoe()

invalid = True
print("*****Welcome to Dan's blackjack simulator!*****")
while invalid:
    number = input("How many players would like to play? ")
    try:
        number = int(number)
    except ValueError:
        number = input("Please enter only integers (Press 'Enter' to continue)")
    else:
        if number > 0:
            if number > 6:
                print("This game only supports 1 to 6 players")
            else:
                while invalid:
                    min_bet = input("What would you like the minimum bet to be? ")
                    try:
                        min_bet = int(min_bet)
                    except ValueError:
                        min_bet = input("Please enter only integers (Press 'Enter' to continue)")
                    else:
                        if min_bet < 5 or min_bet % 5 != 0:
                            print("Minumum bet must be a multiple of $5")
                        else:
                            invalid = False
                game = True
                bj = blackjack(number, min_bet)
                bj.shuffle_deck()
        else:
            print("Well, if no one wants to play you can just close this program.")
            invalid = False
            
while game:
    print("What would you like to do next?")
    response = input("(P)lay another round, (N)umber of players, (C)hange a " +
        "player's bet, (S)imulate rounds, (E)xit: ")
    if (
            response.lower() == 'p' or 
            response.lower() == "play" or 
            response.lower() == "play another round"
    ):
        for player in bj.players:
            if player['bankroll'] < bj.min_bet:
                valid = False
                print(f"{player['name']}, " + 
                  "you don't have enough money to play this round")
                while not(valid):
                    buyIn = input("Would you like to buy back in? ")
                    if buyIn.lower() == 'y' or buyIn == 'yes':
                        amount = input("How much would you like to add? ")
                        try:
                            amount = int(amount)
                        except ValueError:
                            print("Press 'Enter' to continue")
                            amount = input("Enter an integer amount only ")
                        else:
                            player['bankroll'] += amount
                            valid = True
                    elif buyIn.lower() == 'n' or 'no':
                        print("***Need to add code to remove this player***")
                        valid = True
                    else:
                        print("Please enter 'y' or 'n' ")
        bj.play_round()
    elif (
            response.lower() == 'n' or 
            response.lower() == "number" or
            response.lower() == "number of players"
    ):
        Print("Note: Changing the number of players will reset any progress " +
            "on the current game")
        answer = True
        while answer:
            p = input("How many players would you like? (Enter 'c' to cancel)")
            if type(p) == int:
                if p < 0 or p > 6:
                    print("Please select between 1 and 6 players")
                else:
                    print(f"A new game with {p} players has started!")
                    bj = blackjack(p, min_bet)
                    answer = False
    elif (
            response.lower() == 'c' or
            response.lower() == "change" or
            response.lower() == "change a player's bet" or
            response.lower() == "change a players bet"
    ):
        invalid_player = True
        invalid_bet = True
        p = None
        bet = None
        while invalid_player:
            p = input("Which player would like to change their bet? ")
            try:
                p = int(p)
            except ValuieError:
                print("Press 'Enter' to continue")
                p = input("Enter an integer amount only ")
            else:
                if p < 1 or p > bj.number_of_players:
                    print(f"Please enter a position between 1 and {bj.number_of_players}")
                    continue
                else:
                    invalid_player = False
        while invalid_bet:
            bet = input("What should their new bet be? ")
            try:
                bet = int(bet)
            except ValueError:
                print("Press 'Enter' to continue")
                bet = input("Please enter integer multiples of 5 only ")
            else:
                if (bet%5 == 0):
                    if (bet < bj.min_bet):
                        print(f"The minimum bet for this game is {bj.min_bet}")
                    else:
                        confirm = input("Would you like to change to change " +
                          f"{bj.players[p-1]['name']}'s bet to {bet}? ")
                        if confirm.lower() == 'y' or confirm.lower() == "yes":
                            print(f"{bj.players[p-1]['name']}'s bet has been" +
                              f" changed to {bet}")
                            bj.players[p-1]['bet'] = bet
                            invalid_bet = False
                        else:
                            print("No bet change has been made")
                            invalid_bet = False
                else:
                    print("Please enter only multiples of 5 for the bet amount")
    elif (
            response.lower() == 's' or
            response.lower() == "simulate" or 
            response.lower() == "simulate rounds"
    ):
        print("Sorry, we are still working on this feature. Please check " +
            "back later")
    elif (
            response.lower() == 'e' or 
            response.lower() == 'exit' or
            response.lower() =='q' or
            response.lower() == "quit" or 
            response.lower() == 'x'
    ):
        game = False
    else:
        print("I'm sorry, I didn't understand your command")
