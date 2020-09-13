"""Class to run a game of Bridge.
"""
from Deck import Deck
from Player import Player
from Board import Board
from Card import Card

from random import randint            # Generates a random board number
import numpy as np                    # Used for storing data
import matplotlib.pyplot as plt       # Plotting images
import pandas as pd

class Game:
	"""A singular game of bridge with a board of cards, and players. They bid then are scored based on how they perform. This can then be used in a genetic algorithm hopefully.
	
	Attributes:
	    BID_NAMES (list): names of possible bids in order.
	    bid_sequence (np.ndarray): The sequence of bids made during bidding.
	    board (Board): The board of cards for the game.
	    contract (str): Determined by the bidding, this controls how many points the game is worth, and the trump suit.
	    declerer (int): Declerer is the player who won the contract.
	    opener (int): Index for the opener (to the left of the declerer).
	    play_sequence (np.ndarray): The cards played during a game.
	    players (list): The players playing the game. (AI or Human)
	    trumps (int): Description
	    win_record (list): Description
	"""


	def __init__(self, boardno = randint(1,17), players = [Player(), Player(), Player(), Player()]):
		"""A singular game of bridge with a board of cards, and players. They bid then are scored based on how they perform. This can then be used in a genetic algorithm hopefully.
		
		Args:
		    boardno (int, optional): For selecting boards we use the board number.
		    players (list, optional): The specific player bots who are playing the game.
		"""
		self.board         = Board(boardno = boardno)
		self.players       = players
		self.bid_sequence  = np.zeros((38,38), dtype=np.float64)
		self.play_sequence = np.zeros((52,52), dtype=np.float64)
		self.BID_NAMES     = ['P','X','XX'] + [str(n)+suit for n in range(1,8) for suit in ['C', 'D', 'H', 'S', 'NT']]
		self.win_record    = []

		self.hands = self.board.deal_hands()

		self.unshuffled_deck = Deck()


		for i in range(4):
			players[i].add_cards(self.hands[i])

	def run_game(self):
		"""Runs the game from bidding to play to evaluation.
		"""
		self.run_bidding()
		if self.contract != -1:
			self.run_play()
			self.score = self.run_evaluation()
		else:
			self.score = 0
		self.assign_points()

###############################################################################
##--------------------------- Bidding Functions -----------------------------##
###############################################################################

	def run_bidding(self):
		"""Function to run the bidding phase of a game.
		"""

		bidding_active = True
		i = self.board.dealer

		while bidding_active == True:
			# Select the player who is bidding.
			player = self.players[i % 4]

			# Tell a player what has been bid and ask them to bid something.
			bid = player.decide_bid(self.bid_sequence, self.board.boardno)

			# Save the bid to memory.
			self.add_bid(bid,i)

			# Check for next round of bidding.
			bidding_active = self.should_we_continue_bidding(i)

			# Increase the iterations to
			i += 1

		self.determine_contract()

	def determine_contract(self):
		"""Looks at the bidding sequence and determines a contract.
		"""
		bids         = self.bid_sequence
		bid_sequence = np.argmax(bids, axis = 0)
		if len(bid_sequence) == 0:
			self.contract =  -3
			self.trumps   = -3
		else:
			self.contract = (max(bid_sequence) - 3) // 5
			self.trumps   = (max(bid_sequence) - 3) % 5


		self.declerer = (self.board.dealer + np.argmax(bid_sequence)) % 4
		self.opener   = self.declerer + 1

	def should_we_continue_bidding(self, i):
		"""Looks at the bidding sequence and determines if bidding is complete.
		
		Args:
		    i (int): what bid has been made.
		
		Returns:
		    bool: Evaluation to continue bidding or not.
		"""
		bids         = self.bid_sequence
		n_bids       = i
		bid_sequence = np.argmax(bids, axis = 0)
		bid_sequence = bid_sequence[:n_bids]
		
		# If 38 bids have been made
		if n_bids == 37:
			return False

		# If the last 3 bids have been passes.
		if len(bid_sequence)>3:
			if all(bid_sequence[-3:] == [0,0,0]):
				return False

		return True

	def add_bid(self, bid, i):
		"""Adds a bid to the bidding sequence.
		
		Args:
		    bid (int): Index of bid made.
		    i (int): Index of when bid was made.
		"""
		self.bid_sequence[bid,i] = 1

	def plot_bidding(self, savefig = False, savefig_name = ''):
		"""Plots an image of the bidding sequence.
		
		Args:
		    savefig (bool, optional): Should we save the image to file.
		    savefig_name (str, optional): Filename of where to save image.
		"""
		plt.figure(figsize = (10,10))
		plt.imshow(self.bid_sequence)
		plt.title("Bidding Sequence")
		plt.xlabel("Time")
		plt.ylabel("Bids made")
		plt.yticks(ticks = range(len(self.BID_NAMES)), labels = self.BID_NAMES)
		if savefig:
			plt.savefig(savefig_name)
		# plt.show()
		plt.close()

###############################################################################
##-------------------------- Card Play Functions ----------------------------##
###############################################################################

	def run_play(self):
		"""Runs the playing of cards section of the game.
		"""
		opener = self.opener.copy()
		i = 0
		for roundno in range(13):
			for playerno in range(4):
				# Select which player is playing.
				player = self.players[playerno % 4]

				# Dummpy is played by declerer.
				if playerno % 2 == self.declerer % 2:
					player = self.players[self.declerer]
					
				# Ask the player which card they want to play.
				card   = player.decide_card(self.bid_sequence, self.play_sequence, self.board.boardno)
				
				# Update the play_sequence array.
				self.update_play_sequence(card,i)

				i += 1
			opener = self.who_won_round(roundno)
			self.win_record += [opener]

	def update_play_sequence(self, card, i):
		"""Adds a bid to the bidding sequence.
		
		Args:
		    card (TYPE): Description
		    i (int): Index of when bid was made.
		
		Deleted Parameters:
		    bid (int): Index of bid made.
		"""
		self.play_sequence[card,i] = 1

	def plot_card_play(self, savefig = False, savefig_name = ''):
		"""Plots an image of the card play sequence.
		
		Args:
		    savefig (bool, optional): Should we save the image to file.
		    savefig_name (str, optional): Filename of where to save image.
		"""
		plt.figure(figsize = (10,10))
		plt.imshow(self.play_sequence)
		plt.title("Play Sequence")
		plt.xlabel("Time")
		plt.ylabel("Cards Played")
		if savefig:
			plt.savefig(savefig_name)
		# plt.show()
		plt.close()

	def who_won_round(self, roundno):
		"""Summary
		
		Args:
		    roundno (int): The round of the game we are currently playing.
		
		Returns:
		    int: Which player won this round.
		"""
		play = np.argmax(self.play_sequence, axis = 0)
		last_round = play[4*roundno:4*(roundno+1)]

		if len(self.win_record) == 0:
			opener = self.opener
		else:
			opener = self.win_record[-1]

		opened_suit   = last_round[0] // 13
		followed_suit = [last_round[0] // 13 == play // 13 for play in last_round]
		trumped       = [self.trumps == play // 13 for play in last_round]


		winner = opener
		for i in range(opener,opener + 4):
			if (followed_suit[i % 4] and
			   (not any(trumped)) and
			   (last_round[i % 4] > last_round[winner % 4])):
				winner = i
			if trumped[i % 4] and (last_round[i % 4] > last_round[winner % 4]):
				winner = i
		return 	winner % 4

###############################################################################
##------------------------- Evaluation Functions ----------------------------##
###############################################################################

	def run_evaluation(self):
		"""Summary
		"""
		# Count number of tricks made
		did_it_make        = [(i + self.declerer) % 2 == 0 for i in self.win_record]
		number_tricks_made = sum(did_it_make)

		number_tricks_made += self.bidding_error_counter()
		number_tricks_made += self.playing_error_counter()

		if number_tricks_made > 13:
			number_tricks_made = 13
		if number_tricks_made < 0:
			number_tricks_made = 0

		# Difference between what was made and what was bid.
		diff = number_tricks_made - (self.contract + 7)

		# Load score table.
		score_table = pd.read_csv('../data/scores.csv')
		score_table = score_table.set_index('Unnamed: 0')

		points = score_table.loc[self.BID_NAMES[self.contract*5+3+self.trumps],str(diff)]

		return points

	def assign_points(self):
		for i in range(4):
			player = self.players[(i+self.declerer)%4]
			if i%2 == 0:
				player.score_history += [self.score]
			else:
				player.score_history += [-self.score]
			player.score = np.mean(player.score_history)

	def bidding_error_counter(self):
		"""Summary
		
		Returns:
		    int: Number of invalid bids made by declerer more than defence.
		"""
		bids = self.bid_sequence

		# Bids have to be higher than bid before. (but can be pass or doubles)
		high_bid = 2
		valid_record = []
		for i in range(len(bids[0])):
			bid = np.argmax(bids[:,i])
			if bid <= high_bid and bid > 2:
				valid_record += [2]
			else:
				valid_record += [0]
				high_bid = bid

		invalid_declerer = sum(valid_record[self.declerer % 2::2])
		invalid_defence  = sum(valid_record[(self.declerer + 1) % 2::2])
		
		return invalid_defence - invalid_declerer

	def playing_error_counter(self):
		"""Summary
		
		Returns:
		    int: Number of invalid plays made by declerer more than defence.
		"""

		play = np.argmax(self.play_sequence, axis = 0)
		playernos = []
		invalid_declerer = []
		invalid_defence = []

		opener = self.opener.copy()
		for roundno in range(1,13):
			# They need to follow suit.
			cards_played = play[4*roundno:4*(roundno+1)]
			followed_suit = [cards_played[0] // 13 == card // 13 for card in cards_played]

			# They also need to have the card in their hand.
			# 1. they were dealt the card.
			card_dealt = []
			# 2. they haven't played the card before.
			not_played_before = []
			for i in range(4):
				playerno = (opener + i) % 4
				playernos += [playerno]
				card = self.unshuffled_deck.cards[play[roundno*4+i]]

				card_dealt += [card in self.hands[i].cards]

				past_plays = []
				for j in range(len(playernos)-1):
					if playernos[j] == playerno:
						past_plays += [play[j]]
				not_played_before += [play[roundno*4+i] not in past_plays]


			for i in range(4):
				playerno = (opener + i) % 4

				if playerno % 2 == self.declerer % 2:
					invalid_declerer += [not_played_before[i] and followed_suit[i] and card_dealt[i]]
				else:
					invalid_defence  += [not_played_before[i] and followed_suit[i] and card_dealt[i]]
			if len(self.win_record) !=13:
				print(len(self.win_record), roundno)
			opener = self.win_record[roundno]

		invalid_declerer = -sum(invalid_declerer)
		invalid_defence  = -sum(invalid_defence)

		
		return invalid_defence - invalid_declerer