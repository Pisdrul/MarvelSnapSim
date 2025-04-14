from cards import Card

class Cable(Card):
    def __init__(self, ally, status):
        super().__init__(2, 3, "Cable", ally, status)
        self.description = "On Reveal: Draw a card from the opponent's deck"
    
    def onReveal(self, locationlist):
        if self.ally:
            if len(self.status["enemydeck"]) != 0:
                self.status["allyhand"].append(self.status["enemydeck"][-1])
                self.status["enemydeck"].pop().ally = True
        else:
            if len(self.status["allydeck"]) != 0:
                self.status["enemyhand"].append(self.status["allydeck"][-1])
                self.status["allydeck"].pop().ally = False