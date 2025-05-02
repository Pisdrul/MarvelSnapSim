from Locations import Location

class LakeHeldas(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Lake Heldas"
        self.description = "Cards that cost 1 have +2 Power here"
    
    def applyOngoing(self, location):
        for unit in self.allies + self.enemies:
            if unit.base_cost == 1:
                unit.ongoing_to_apply.append(self)
    
    def ongoing(self, unit):
        unit.ongoing_buff +=2