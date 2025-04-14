from cards import Card, random

class Korg(Card):
    def __init__(self, ally, status):
        super().__init__(1, 2, "Korg", ally, status)
        self.description = "On Reveal: Shuffle a Rock into the opponent's deck"
    
    class Rock(Card):
        def __init__(self, ally, status):
            super().__init__(1, 0, "Rock", ally, status)
            self.description = "Rock!"
    
    def onReveal(self, locationlist):
        if not self.ally:
            rock = self.Rock(not self.ally, self.status)
            self.status["allydeck"].insert(random.randint(0, len(self.status["allydeck"])), rock)
        else:
            rock = self.Rock(not self.ally, self.status)
            self.status["enemydeck"].insert(random.randint(0, len(self.status["enemydeck"])), rock)