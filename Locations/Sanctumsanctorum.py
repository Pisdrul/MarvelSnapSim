from Locations import Location

class Sanctumsanctorum(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Sanctum Sanctorum"
        self.description = "Cards can't be played here"
        self.can_play_cards_base = False
