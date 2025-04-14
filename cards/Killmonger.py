from cards import Card

class Killmonger(Card):
    def __init__(self, ally, status):
        super().__init__(3, 3, "Killmonger", ally, status)
        self.description = "On Reveal: Destroy ALL 1-cost cards"
    
    def onReveal(self, locationlist):
        for location in locationlist.values():
            for card in location.allies + location.enemies:
                if card.base_cost == 1:
                    location.destroyCard(card)
        