from cards import Card

class Infinaut(Card):
    def __init__(self, ally, status):
        super().__init__(6, 20, "The Infinaut", ally, status)
        self.description = "If you played a card last turn, you can't play this"
    
    def updateCard(self, locationlist):
        super().updateCard(locationlist)
        self.can_be_played = True
        for cards in self.status["cardsplayed"]:
            print(cards)
            if cards[0].ally == self.ally and cards[1] == self.status["turncounter"]-1:
                self.can_be_played = False