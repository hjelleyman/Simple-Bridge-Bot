from Card import Card
from Hand import Hand
from random import shuffle

class Deck:
	"""Deck of cards
	
	All of the cards.
	"""

	def __init__(self):
		self.cards = [Card(rank, suit) for rank in range(13) for suit in range(4)]


	def __str__(self):
		cards = ''
		for card in self.cards:
			cards += str(card) + '\n'
		return cards

	def shuffle(self):
		"""Shuffles the cards"""
		shuffle(self.cards)

	def deal(self, hand_names):
		hands = []
		i = 0
		for hand_name in hand_names:
			hand = Hand(hand_name)
			hand.add_cards(self.cards[i*len(self.cards)//len(hand_names):(i+1)*len(self.cards)//len(hand_names)])
			hands += [hand]
		return hands