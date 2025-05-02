from Locations import Location

class Jotunheim(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Jotunheim"
        self.description = "After each turn, cards here lose 1 Power"
    
    def endOfTurn(self):
        super().endOfTurn()
        for unit in self.allies + self.enemies:
            unit.onreveal_buff -= 1