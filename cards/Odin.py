from cards import Card

class Odin(Card):
    def __init__(self, ally, status):
        super().__init__(6, 8, "Odin", ally, status)
        self.description = "On Reveal: Repeat the On Reveal abilities of your other cards here"
        self.onreveallimit = 32
        self.counter = 0 
    
    def onReveal(self, locationlist):
        if self.ally:
            cur = self.location.allies
        else:
            cur = self.location.enemies
        for unit in cur:
            if unit != self:
                self.counter += 1
                unit.onReveal(locationlist)
            if self.counter >= self.onreveallimit:
                break
    
    def endOfTurn(self):
        self.counter =0