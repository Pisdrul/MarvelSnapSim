from cards import Card
class Death(Card):
    def __init__(self, ally, status):
        super().__init__(8, 12, "Death", ally, status)
        self.description = "Costs 1 less for each card that was destroyed this game"
    
    def updateCard(self,locationlist):
        super().updateCard(locationlist)
        self.cur_cost = 12 - len(self.status["alliesdestroyed"]) - len(self.status["enemiesdestroyed"])