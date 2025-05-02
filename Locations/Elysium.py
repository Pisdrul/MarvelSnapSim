from Locations import Location

class Elysium(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Elysium"
        self.description = "Cards cost 1 less"
    
    def applyOngoing(self, locationlist):
        for cards in self.status["allyhand"] + self.status["enemyhand"]:
            cards.ongoing_to_apply.append(self)
    
    def ongoing(self, card):
        card.cost_ongoing -= 1