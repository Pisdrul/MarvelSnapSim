from cards import Card
import copy, random

class WhiteQueen(Card):
    def __init__(self, ally, status):
        super().__init__(3, 4, "White Queen", ally, status)
        self.description= "On Reveal: Copy the card that costs the most from your opponent's hand into your hand."

    def onReveal(self, locationlist):
        if self.ally:
            max_cost = max(obj.cur_cost for obj in self.status["enemyhand"])
            max_cost_items = [obj for obj in self.status["enemyhand"] if obj.cur_cost == max_cost]
            self.status["allyhand"].append(copy.deepcopy(random.choice(max_cost_items)))
        else:
            max_cost = max(obj.cur_cost for obj in self.status["allyhand"])
            max_cost_items = [obj for obj in self.status["allyhand"] if obj.cur_cost == max_cost]
            self.status["enemyhand"].append(copy.deepcopy(random.choice(max_cost_items))) 
