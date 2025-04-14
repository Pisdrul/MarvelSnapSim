from cards import Card

class Nightcrawler(Card):
    def __init__(self, ally, status):
        super().__init__(1, 2, "Nightcrawler", ally, status)
        self.description = "You can move this card once"
        self.moves_number = 1