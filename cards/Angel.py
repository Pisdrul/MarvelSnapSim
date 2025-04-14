from cards import Card

class Angel(Card):
    def __init__(self, ally, status):
        super().__init__(2, 3, "Angel", ally, status)
        self.description = "When one of your cards is destroyed, this flies out of your hand or deck to replace it."
        self.activate_on_destroy = True
    
    def activateOnDestroy(self, card, location):
        if self.ally and card.ally:
            print("Adding angel!")
            try:
                self.status["allyhand"].remove(self)
            except: pass
            try:
                self.status["allydeck"].remove(self)
            except: pass
            if len(location.allies)<4: location.allies.append(self)
        elif not self.ally and not card.ally:
            try:
                self.status["enemyhand"].remove(self)
            except: pass
            try:
                self.status["enemydeck"].remove(self)
            except: pass
            if len(location.enemies)<4: location.enemies.append(self)