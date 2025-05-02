from Locations import Location 
class Mojoworld(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Mojoworld"
        self.description = "Whoever has more cards here gets +100 Power"
    
    def applyOngoing(self, locationlist):
        self.ongoing_to_apply.append(self)
    
    def ongoing(self, location):
        if len(location.allies) > len(location.enemies):
            self.allies_power_buff_sum += 100
        elif len(location.allies) < len(location.enemies):
            self.enemies_power_buff_sum += 100
