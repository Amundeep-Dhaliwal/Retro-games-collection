#!python3

import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs') # this a tuple, so is the ranks
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9,
          'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card: # card(): is also acceptable, parentheses required for inheritance

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return 'The deck has: ' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:
	def __init__(self):
		self.cards = [] # empty list for cards in players hand
		self.values = 0 # cards values in the players hand
		self.aces = 0 # number of aces in the players hand

	def add_card(self, card): # card passed in is going to be from the deck
		self.cards.append(card)
		self.values += values[card.rank]

		if card.rank == 'Ace':
			self.aces += 1

	def adjust_for_ace(self):

		while self.values > 21 and self.aces: # any non-zero integer can be treated as the True boolean
			self.values -= 10
			self.aces -= 1




class Chips:
	def __init__(self):
		self.total = 100
		self.bet = 0

	def win_bet(self):
		self.total += self.bet

	def lose_bet(self):
		self.total -= self.bet

def take_bet(chips):

	while True:

		try:
			chips.bet = int(input('How many chips would you like to bet? '))
		except ValueError:
			print('Sorry please provide an integer for the number of chips')
			continue
		else:
			if chips.bet > chips.total:
				print(f'Sorry you do not have enough chips to place that bet! You have: {chips.total} chips')
				continue
			else:
				break

def hit(deck, hand):

	single_card = deck.deal()
	hand.add_card(single_card)
	hand.adjust_for_ace()

def hit_or_stand(deck, hand):
	global playing

	while True:
		x = input('\nHit or Stand? (h/s) ')

		if x.lower().startswith('h'):
			hit(deck,hand)

		elif x.lower().startswith('s'):
			print('Player stands, dealers turn:')
			playing = False

		else:
			print('Sorry, I did not understand, please enter h or s only!')
			continue

		break

def show_some(player,dealer):

	print('\nDealers hand:')
	print('One card hidden')
	print(dealer.cards[1])
	print('\n')
	print('Players hand:')
	for card in player.cards:
		print(card)

def show_all(player, dealer):

	print('\nDealer hand:')
	for card in dealer.cards:
		print(card)
	print('\n')
	print('Players hand:')
	for card in player.cards:
		print(card)



def player_bust(player, dealer, chips):
	print('\nBust: Player')
	chips.lose_bet()

def player_wins(player, dealer, chips):
	print('\nWin: Player')
	chips.win_bet()

def dealer_bust(player, dealer, chips):
	print('\nWin: Player, dealer busted!')
	chips.win_bet()

def dealer_wins(player, dealer, chips):
    print('\nWin: Dealer')
    chips.lose_bet()
	
def push(player, dealer):
	print('\nDealer and player tie! Push.')

while True:
    games_played = 1
    print('Welcome to 21 Blackjack')

    player_chips = Chips()
    print(f'You have: {player_chips.total} chips')

    while playing:

        deck = Deck()
        deck.shuffle()

        player_hand = Hand()
        player_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())

        dealer_hand = Hand()
        dealer_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())


        take_bet(player_chips)

        show_some(player_hand, dealer_hand)

        while playing and player_hand.values < 21:
            hit_or_stand(deck, player_hand)
		# player has the choice to either hit or stand with the cards they have
            show_some(player_hand,dealer_hand)
		# shows the new card the player has acquired (if any)

        if player_hand.values > 21:
            player_bust(player_hand, dealer_hand, player_chips)


        if player_hand.values <= 21:

            while dealer_hand.values < player_hand.values:
                hit(deck, dealer_hand)

            show_all(player_hand, dealer_hand)

            if dealer_hand.values > 21:
                dealer_bust(player_hand, dealer_hand, player_chips)

            elif dealer_hand.values > player_hand.values:
                dealer_wins(player_hand, dealer_hand, player_chips)

            elif player_hand.values > dealer_hand.values:
                player_wins(player_hand,dealer_hand,player_chips)

            else:
                push(player_hand, dealer_hand)

        print(f'\nPlayer total chips are: {player_chips.total}')

        new_game = input('Do you want to play again? (Y/N) ').lower().startswith('y')

        if new_game:
            playing = True
            games_played +=1
            continue
        else:
            print(f'Thank you for playing! You played {games_played} times!')
            break
    break


