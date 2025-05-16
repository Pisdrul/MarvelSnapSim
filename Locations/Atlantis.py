from Locations import Location

class Atlantis(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Atlantis"
        self.description = "If you only have one card here, it has +5 Power"

    def applyOngoing(self, locationlist):
        if len(self.allies) == 1:
            self.allies[0].ongoing_to_apply.append(self)
        if len(self.enemies) == 1:
            self.enemies[0].ongoing_to_apply.append(self)
    
    def ongoing(self, cardOrLocation):
        cardOrLocation.ongoing_buff += 5