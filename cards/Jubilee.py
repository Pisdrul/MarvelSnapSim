from cards import Card

class Jubilee(Card):
    def __init__(self, ally, status):
        super().__init__(4, 1, "Jubilee", ally, status)
        self.description = "On Reveal: Add the top card of your deck to this location."
    
    def onReveal(self, locationlist):
        if self.ally and len(self.status["allydeck"]) > 0 and (len(self.location.allies) + len(self.location.preRevealAllies)) < 4:
            newcard = self.status["allydeck"].pop(0)
            newcard.playCard(self.location)
            newcard.onReveal(locationlist)
        elif not self.ally and len(self.status["enemydeck"]) > 0 and (len(self.location.enemies) + len(self.location.preRevealEnemies)) < 4:
            newcard = self.status["enemydeck"].pop(0)
            newcard.playCard(self.location)
            newcard.onReveal(locationlist)