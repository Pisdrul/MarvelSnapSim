from Locations import Location

class AsteroidM(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Asteroid M"
        self.description = "After you play a 3 or 4 cost card, move it here"
    
    def onPlayEffect(self, card):
        if (card.cost == 3 or card.cost == 4) and not self.checkIfLocationFull(card.ally):
            card.move(self)