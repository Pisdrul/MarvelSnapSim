from cards import Card

class Uatu(Card):
    def __init__(self, ally, status):
        super().__init__(1, 2, "Uatu the Watcher", ally, status)
        self.description = "Game start: You can see the unrevealed locations"
    
    def startOfGame(self, locationlist):
        self.activate_in_deck = True
    
    def updateCard(self, locationlist):
        super().updateCard(locationlist)
        """Reveal the unrevealed locations."""
        print("Uatu is telling you that:")
        for location in locationlist.values():
            if location.temporary:
                print(f"Location {location.locationNum} will turn into: {location.newLoc.name}")