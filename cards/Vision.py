from cards import Card

class Vision(Card):
    def __init__(self, ally, status):
        super().__init__(5, 8, "Vision", ally, status)
        self.description = "You can move this card every turn"
        self.moves_number = 100