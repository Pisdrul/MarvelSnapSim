from cards import Card
class Psylocke(Card):
    def __init__(self, ally, status):
        super().__init__(2,1, "Psylocke", ally, status)
        self.description = "On reveal: +1 energy next turn"
    
    def onReveal(self, locationlist):
        if self.ally:
            self.status["tempenergyally"] +=1
        else:
            self.status["tempenergyenemy"] +=1
        print("+1 energy next turn!")