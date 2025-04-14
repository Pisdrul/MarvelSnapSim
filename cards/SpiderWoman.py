from cards import Card

class SpiderWoman(Card):
    def __init__(self, ally, status):
        super().__init__(5, 8, "Spider-Woman", ally, status)
        self.description = "On Reveal: Afflict all enemy cards here with -1 power."
    
    def onReveal(self, locationlist):
        if self.ally:
            for unit in self.location.enemies:
                unit.onreveal_buff -= 1
        else:
            for unit in self.location.allies:
                unit.onreveal_buff -= 1
