from cards import Card

class Hawkeye(Card):
    def __init__(self, ally, status):
        super().__init__(1, 1, "Hawkeye", ally, status)
        self.description = "On Reveal: If you play a card at this location next turn, +3 Power"
        self.turnToCheck = 0
        self.onRevealNum = 0
    
    def onReveal(self, locationlist):
        self.onRevealNum += 1
        self.turnToCheck = self.status["turncounter"] + 1
        self.locationNumToCheck = self.location.locationNum
    
    def endOfTurn(self):
        check = False
        if self.status["turncounter"] == self.turnToCheck and self.onRevealNum != 0:
            for cardPlayed in self.status["cardsplayed"]:
                if cardPlayed[1] == self.turnToCheck and cardPlayed[2] == self.locationNumToCheck and cardPlayed[0].ally == self.ally:
                    check = True
                    break
            if check:
                print("Buffing Hawkeye!")
                self.onreveal_buff += 3*self.onRevealNum
