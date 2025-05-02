from Locations import Location 
class Onslaughtcitadel(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Onslaught Citadel"
        self.description = "Ongoing effects here are doubled"
        self.ongoing_number_base = 2
