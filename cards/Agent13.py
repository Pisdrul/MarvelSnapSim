from cards import Card
import random
import sys, inspect
import flask

class Agent13(Card):
    def __init__(self, ally, status):
        super().__init__(1, 2, "Agent 13", ally, status)
        self.description = "On Reveal: Add a random card to your hand."
    def randomCard(self):
        current_module = sys.modules[__name__]
        classes = [cls for name, cls in inspect.getmembers(current_module, inspect.isclass)
                if cls.__module__ == __name__]
        return random.choice(classes)(self.ally, self.status)

    def onReveal(self, locationlist):
        if self.ally: 
            self.status["allyhand"].append(self.randomCard())
        else:
            self.status["enemyhand"].append(self.randomCard())
    
    def render(self):
        return flask.url_for('static', filename='assets/Agent13.webp')