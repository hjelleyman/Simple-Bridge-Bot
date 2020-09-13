class Hand:
    """A labeled collection of cards usually held by a single player but could be used for other purposes."""

    def __init__(self, label = ""):
        """Creates an empy collection of cards with a label."""

        self.label = label
        self.cards = []

    def add_card(self, card):
        """Adds a card to the hand."""

        self.cards.append(card)

    def add_cards(self, cards):
        """adds a list of cards to a hand"""

        for card in cards:
            self.add_card(card)
