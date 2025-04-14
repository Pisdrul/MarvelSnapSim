from cards import Card
class Yondu(Card):
    def __init__(self, ally, status):
        super().__init__(1, 2, "Yondu", ally, status)
        self.description = "On Reveal: Banish the card that costs the least in your opponent's deck."
    
    def onReveal(self, locationlist):
        if self.ally:
            if len(self.status["enemydeck"]) > 0:
                toBanish = min(self.status["enemydeck"], key=lambda x: x.cost)
                self.status["enemydeck"].remove(toBanish)
                print("Removed ", toBanish.name)
        else:
            if len(self.status["allydeck"]) > 0:
                toBanish = min(self.status["allydeck"], key=lambda x: x.cost)
                self.status["allydeck"].remove(toBanish)
                print("Removed ", toBanish.name)