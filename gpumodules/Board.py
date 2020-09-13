from Deck import Deck

class Board:
	"""Board prepared for playing Bridge."""

	def __init__(self, vulnerability = 'None', dealer = 0, boardno = 0):
		self.deck = Deck()
		self.vulnerability = vulnerability
		self.dealer = dealer
		self.boardno = 0
		self.deal_hands()

	def deal_hands(self):
		self.deck.shuffle()
		Hand_names = [str(i) for i in range(4)]
		hands = self.deck.deal(Hand_names)
		self.hands = hands
		return hands
