from cards import Card

class BuckyBarnes(Card):
    def __init__(self, ally, status):
        super().__init__(2, 1, "Bucky Barnes", ally, status)
        self.description = "When this is destroyed, replace it with the Winter Soldier."
    
    class WinterSoldier(Card):
        def __init__(self, ally, status):
            super().__init__(2, 7, "Winter Soldier", ally, status)
            self.description = "It's time for me to face my past"
    
    def whenDestroyed(self, locationlist):
        if self.ally:
            locationlist["location1"].allies.append(self.WinterSoldier(self.ally, self.status))
        else:
            locationlist["location1"].enemies.append(self.WinterSoldier(self.ally, self.status))