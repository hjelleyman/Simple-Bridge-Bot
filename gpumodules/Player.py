"""Summary
"""
import numpy as np
from random import randint
from Brain2 import Brain, evolve

class Player:
	"""[summary]
	
	[description]
	
	Attributes:
	    bidding_brain (TYPE): Description
	    card_vec (TYPE): Description
	    cards (TYPE): Description
	    playing_brain (TYPE): Description
	
	Deleted Attributes:
	    player (TYPE): Description
	"""
	idno = 0

	def __init__(self, bidding_network = None, playing_network = None):
		"""[summary]
		
		[description]
		
		Args:
		    bidding_network (TYPE): Description
		    playing_network (TYPE): Description
		"""
		if bidding_network == None:
			self.bidding_brain = self.gen_new_bidder()
		else:
			self.bidding_brain = bidding_network

		if playing_network == None:
			self.playing_brain = self.gen_new_player()
		else:
			self.playing_brain = playing_network

		# Starts off with no score
		self.score_history = []
		self.score         = 0

		# Assign idno for each player
		self.idno = Player.idno
		Player.idno = self.idno + 1

	def decide_bid(self, bid_sequence, boardno):
		"""Summary
		
		Args:
		    bid_sequence (TYPE): Description
		    boardno (TYPE): Description
		
		Returns:
		    TYPE: Description
		"""
		play_sequence         = np.zeros(52*52).flatten()
		bid_sequence          = bid_sequence.flatten().copy()
		boardnovec            = np.zeros(16)
		boardnovec[boardno-1] = 1
		vector                = list(play_sequence) + list(bid_sequence) + [boardno] + list(self.card_vec)
		vector                = np.array([vector])

		bid = self.bidding_brain.decide(vector)
		return np.argmax(bid)

	def decide_card(self, bid_sequence, play_sequence, boardno	):
		"""Summary
		
		Args:
		    bid_sequence (TYPE): Description
		    play_sequence (TYPE): Description
		    boardno (TYPE): Description
		
		Returns:
		    TYPE: Description
		"""
		play_sequence         = play_sequence.flatten()
		bid_sequence          = bid_sequence.flatten().copy()
		boardnovec            = np.zeros(16)
		boardnovec[boardno-1] = 1
		vector                = list(play_sequence) + list(bid_sequence) + [boardno] + list(self.card_vec)
		vector                = np.array([vector])

		play = self.playing_brain.decide(vector)
		return np.argmax(play)

	def gen_new_bidder(self):
		"""Summary
		
		Returns:
		    TYPE: Description
		"""
		return Brain(nin = 4201, nout = 38)

	def gen_new_player(self):
		"""Summary
		
		Returns:
		    TYPE: Description
		"""
		return Brain(nin = 4201, nout = 52)

	def add_cards(self, hand):
		"""Summary
		
		Args:
		    hand (TYPE): Description
		"""
		self.cards = hand.cards
		self.card_vec = np.zeros(52)

		for card in self.cards:
			i = card.suit * 13 + card.rank
			self.card_vec[i] = 1

	def copy(self):
		"""Summary
		
		Returns:
		    TYPE: Description
		"""
		bidding_brain = self.bidding_brain.copy()
		playing_brain = self.playing_brain.copy()

		player = Player(bidding_network = bidding_brain, playing_network = playing_brain)

		return player

def evolve_player(player, probabilities = [0.5]*6):
	"""Summary
	
	Args:
	    player (TYPE): Description
	
	Returns:
	    TYPE: Description
	"""
	player = player.copy()
	player.bidding_brain = evolve(player.bidding_brain, probabilities = probabilities[:3])
	player.playing_brain = evolve(player.playing_brain, probabilities = probabilities[3:])

	return player






if __name__ == '__main__':
	player = Player()
	print(player.bidding_brain.arrays)