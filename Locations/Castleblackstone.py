from Locations import Location 
class Castleblackstone(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Castle Blackstone"
        self.description = "The player winning here gets +1 energy each turn"
    
    def startOfTurn(self):
        super().startOfTurn()
        if self.winning == "Ally":
            self.status["tempenergyally"] += 1
        elif self.winning == "Enemy":
            self.status["tempenergyenemy"] += 1