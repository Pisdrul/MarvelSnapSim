from cards import Card
import random
class Elektra(Card):
    def __init__(self, ally, status):
        super().__init__(1, 2, "Elektra", ally, status)
        self.description = "On Reveal: Destroy a 1-cost card on your opponent's side here"
    
    def onReveal(self, locationlist):
        if self.ally:
            if len(self.location.enemies)>0:
                candidates = []
                for unit in self.location.enemies:
                    if unit.base_cost == 1:
                        candidates.append(unit)
                print(len(candidates))
                if len(candidates)==0:
                    print("No candidates!")
                else:
                    tobedestroyed = random.choice(candidates)
                    self.location.destroyCard(tobedestroyed)
        else:
            if len(self.location.allies)>0:
                candidates = []
                for unit in self.location.allies:
                    if unit.base_cost == 1:
                        candidates.append(unit)
                if len(candidates)==0:
                    print("No candidates!")
                else:
                    tobedestroyed = random.choice(candidates)
                    self.location.destroyCard(tobedestroyed)