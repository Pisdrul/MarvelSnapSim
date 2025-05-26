from cards import Card
import random
class Doctorstrange(Card):
    def __init__(self, ally, status):
        super().__init__(2, 3, "Doctor Strange", ally, status)
        self.description = "On Reveal: Move your highest-Power card(s) to this location."
    
    def onReveal(self, locationlist):
        cur_high = -100
        toMove = []
        if self.ally:
            for card in locationlist["location1"].allies + locationlist["location2"].allies + locationlist["location3"].allies:
                if card.location != self.location:
                    if card.cur_power > cur_high:
                        cur_high = card.cur_power
                        toMove = [card]
                    elif card.cur_power == cur_high:
                        toMove.append(card)
        else:
            for card in locationlist["location1"].enemies + locationlist["location2"].enemies + locationlist["location3"].enemies:
                if card.location != self.location:
                    if card.cur_power > cur_high:
                        cur_high = card.cur_power
                        toMove = [card]
                    elif card.cur_power == cur_high:
                        toMove.append(card)
        random.shuffle(toMove)
        for card in toMove:
            if not self.location.checkIfLocationFull(card.ally):
                print(card.name, " moved to ", self.location.name)
                card.move(self.location)
