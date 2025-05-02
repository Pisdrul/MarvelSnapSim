from Locations import Location 
class Kamartaj(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Kamar-Taj"
        self.description = "On reveal effects activate twice here."
        self.on_reveal_number_base = self.on_reveal_number_base * 2
