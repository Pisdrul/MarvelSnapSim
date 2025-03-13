class Card:
    def __init__(self, cost, power, name, ally):
        self.cost = cost
        self.power = power
        self.name = name
        self.location = 0
        self.ally = ally
        self.cur_power = power
        self.has_ongoing = False
        
    def __repr__(self):
        return f"{self.cur_power}"
    
    def onReveal(self):
        print("Revealed ",self.name)
    
    def playCard(self,location):
        self.location= location
    def endOfTurn(self):
        pass
    def checkOngoing(self):
        self.location.checkOngoing(self)
    def setCurPower(self, num):
        self.cur_power = num




class TestCard(Card):
    def __init__(self, cost, power, name, ally):
        super().__init__(cost, power, name, ally)
    def onReveal(self):
        print("Revealing TestCard")
        print("Current power: ", self.power)
        self.power+=2
        print("Increased power to: ", self.power)
    
class EndOfTurnTest(Card):
    def __init__(self, cost, power, name, ally):
        super().__init__(cost, power, name, ally)
        self.counter =0
    def endOfTurn(self):
        print("increasing power of", self.name)
        self.power +=1
        self.counter +=1
        if self.counter >3:
            print(self.name," destroyed itself!")
            self.location.removeCard(self)
class OngoingTest(Card):
    def __init__(self, cost, power, name, ally):
        super().__init__(cost, power, name, ally)
        self.has_ongoing = True

    def ongoing(self,power):
        print('here')
        return power * 2