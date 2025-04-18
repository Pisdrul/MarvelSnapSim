import copy
from cards import Card
class Multipleman(Card):
    def __init__(self, ally, status):
        super().__init__(2, 3, "Multiple Man", ally, status)
        self.description = "When this moves, add a copy to the old location"

    def move(self, newloc):
        if self.ally:
            cur = self.location.allies
            next = newloc.allies
        else: 
            cur = self.location.enemies
            next = newloc.enemies
        if len(next)<4 and newloc != self.location:
            self.location.removeCard(self)
            self.location = newloc
            cur.append(copy.deepcopy(self))
            next.append(self)
            for unit in self.location.allies + self.location.enemies:
                unit.onCardBeingMovedHere()