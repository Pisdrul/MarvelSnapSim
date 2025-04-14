from cards import Card

class Medusa(Card):
    def __init__(self, ally, status):
        super().__init__(2, 2, "Medusa", ally, status)
        self.description = "On Reveal: If this is at the middle location, +3 Power"
    
    def onReveal(self, locationlist):
        if self.location == locationlist["location2"]:
            self.onreveal_buff += 3
            