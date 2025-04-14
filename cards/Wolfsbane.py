from cards import Card

class Wolfsbane(Card):
    def __init__(self, ally, status):
        super().__init__(3, 1, "Wolfsbane", ally, status)
        self.description = "On Reveal: +2 Power for each other card you have here"
    
    def onReveal(self, locationlist):
        if self.ally: 
            self.onreveal_buff += 2*(len(self.location.allies))
        else:
            self.onreveal_buff += 2*(len(self.location.enemies))