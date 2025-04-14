from cards import Card

class Hobgoblin(Card):
    def __init__(self, ally, status):
        super().__init__(5, -8, "Hobgoblin", ally, status)
        self.description = "On Reveal: Switch sides."
    
    def onReveal(self, locationlist):
        if self.ally:
            if len(self.location.enemies) <4:
                self.ally = False       
        else:
            if len(self.location.allies) <4:
                self.ally = True