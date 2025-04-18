from cards import Card

class Americachavez(Card):
    def __init__(self, ally, status):
        super().__init__(1,2, "America Chavez", ally, status)
        self.description = "On Reveal: Give the top card of your deck +2 power"
    
    def onReveal(self, locationlist):
        if self.ally and len(self.status["allydeck"])>0:
            self.status["allydeck"][-1].onreveal_buff += 2
        elif not self.ally and len(self.status["enemydeck"])>0:
            self.status["enemydeck"][-1].onreveal_buff += 2
        print("Increased power of the card on top of the deck by 2!")