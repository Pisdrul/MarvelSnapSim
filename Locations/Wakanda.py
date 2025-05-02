from Locations import Location 
class Wakanda(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Wakanda"
        self.description = "Cards here can't be destroyed"
        self.can_destroy_base = False