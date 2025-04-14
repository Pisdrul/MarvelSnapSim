from cards import Card

class Okoye(Card):
    def __init__(self, ally, status):
        super().__init__(2, 3, "Okoye", ally, status)
        self.description = "On Reveal: Give every card in your deck +1 Power."
    
    def onReveal(self, locationlist):
        if self.ally:
            for card in self.status["allydeck"]:
                card.onreveal_buff += 1
        else:
            for card in self.status["enemydeck"]:
                card.onreveal_buff += 1