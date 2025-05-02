from Locations import Location 
class Barwithnoname(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Bar with no name"
        self.description = "Whoever has the least Power here wins."

    def locationWinner(self):
        if self.alliesPower < self.enemiesPower:
            self.winning = "Ally"
        elif self.alliesPower > self.enemiesPower:
            self.winning = "Enemy"
        else:
            self.winning = "Tie"