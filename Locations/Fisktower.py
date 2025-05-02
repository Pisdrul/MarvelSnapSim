from Locations import Location 

class Fisktower(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Fisk Tower"
        self.description = "When a card moves here, afflict it with -4 Power"
    
    def onCardBeingMoved(self, card):
        if card.location == self:
            card.onreveal_buff -= 4