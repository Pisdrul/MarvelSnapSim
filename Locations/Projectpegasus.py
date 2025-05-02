from Locations import Location

class Projectpegasus(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Project Pegasus"
        self.description = "+5 energy this turn"
    
    def onRevealLocation(self):
        super().onRevealLocation()
        self.status["tempenergyally"] += 5
        self.status["tempenergyenemy"] += 5
