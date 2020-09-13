class Card:
    """A playing card.

    Features:
    -----------
        rank : int
            value of a card.
        suit : int
            suit of a card.
        hcp :
            High card point value of a card based on it's rank.

    Methods:
    -----------
    """

    SUITS = [i for i in range(4)   ]
    RANKS = [i for i in range(1,14)]

    def __init__(self, rank, suit):
        """Creates a playing card."""
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return 'Card {:.0f} of suit {:.0f}'.format(self.rank, self.suit)

    def __eq__(self, other):
        return ((self.rank, self.suit) == (other.rank, other.suit))