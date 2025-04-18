from cards import Card
import random

class Wolverine(Card):
    def __init__(self, ally, status):
        super().__init__(2, 3, "Wolverine", ally, status)
        self.description = "When this card is destroyed or discarded, regenerate it with +2 Power at a random location"
    
    def whenDestroyed(self, locationlist):
        self.regenerate()
    def whenDiscarded(self):
        self.regenerate()

    def regenerate(self):
        locationsNotFull = self.location.locationsThatArentfull(self.ally)
        print(locationsNotFull)
        if len(locationsNotFull) > 0:
            location = random.choice(locationsNotFull)
            if self.ally:
                location.allies.append(self)
            else:
                location.enemies.append(self)
            self.location = location
            self.onreveal_buff += 2