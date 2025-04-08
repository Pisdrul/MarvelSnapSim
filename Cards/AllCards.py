from Cards.Card import Card
from Locations.AllLocations import *
import copy
import random
import sys, inspect
class Magik(Card):
    def __init__(self, ally, status):
        super().__init__(3, 2, "Magik", ally, status)
    
    def onReveal(self,locationlist):
        if self.status["turncounter"] <=5:
            newloc = Limbo(0,self.status, locationlist)
            self.location.changeLocation(newloc)

        else:
            print("doesnt work after turn 5!")

class Sunspot(Card):
    def __init__(self, ally, status):
        super().__init__(1,0, "Sunspot", ally, status)
        self.description = "At the end of the turn, gain power equals to the amount of your unspent energy this turn"
    def endOfTurn(self):
        if self.ally:
            self.onreveal_buff += self.status["allyenergy"]
        else:
            self.onreveal_buff += self.status["enemyenergy"]

class Psylocke(Card):
    def __init__(self, ally, status):
        super().__init__(2,1, "Psylocke", ally, status)
        self.description = "On reveal: +1 energy next turn"
    
    def onReveal(self, locationlist):
        if self.ally:
            self.status["tempenergyally"] +=1
        else:
            self.status["tempenergyenemy"] +=1
        print("+1 energy next turn!")

class AmericaChavez(Card):
    def __init__(self, ally, status):
        super().__init__(1,2, "America Chavez", ally, status)
        self.description = "On Reveal: Give the top card of your deck +2 power"
    
    def onReveal(self, locationlist):
        if self.ally:
            self.status["allydeck"][-1].onreveal_buff += 2
        else:
            self.status["enemydeck"][-1].onreveal_buff += 2
        print("Increased power of the card on top of the deck by 2!")

class Elektra(Card):
    def __init__(self, ally, status):
        super().__init__(1, 2, "Elektra", ally, status)
        self.description = "On Reveal: Replace this location with Limbo. Does not work after turn 5"
    
    def onReveal(self, locationlist):
        if self.ally:
            if len(self.location.enemies)>0:
                candidates = []
                for unit in self.location.enemies:
                    if unit.cost == 1:
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
                    if unit.cost == 1:
                        candidates.append(unit)
                if len(candidates)==0:
                    print("No candidates!")
                else:
                    tobedestroyed = random.choice(candidates)
                    self.location.destroyCard(tobedestroyed)

class Death(Card):
    def __init__(self, ally, status):
        super().__init__(8, 12, "Death", ally, status)
        self.description = "Costs 1 less for each card that was destroyed this game"
    
    def updateCard(self):
        super().updateCard()
        self.cost = 12 - len(self.status["alliesdestroyed"]) - len(self.status["enemiesdestroyed"])

class Knull(Card):
    def __init__(self, ally, status):
        super().__init__(1, 0, "Knull", ally, status)
        self.has_ongoing = True
        self.description = "Ongoing: Has the combined attack of all destroyed cards"
    
    def ongoing(self,card):
        for unit in self.status["alliesdestroyed"] + self.status["enemiesdestroyed"]:
            print("Adding ", unit.cur_power," to Knull")
            self.ongoing_buff += unit.cur_power
    
    def applyOngoing(self, locationlist):
        self.ongoing_to_apply.append(self)

class Sentinel(Card):
    def __init__(self, ally, status):
        super().__init__(2, 3, "Sentinel", ally, status)
        self.description = "On Reveal: Add another Sentinel card to your hand"

    def onReveal(self, locationlist):
        if self.ally:
            self.status["allyhand"].append(Sentinel(self.ally, self.status))
        else:
            self.status["enemyhand"].append(Sentinel(self.ally, self.status))
        
        print("Added another Sentinel card to your hand")

class StarLord(Card):
    def __init__(self, ally, status):
        super().__init__(2, 2, "Star Lord", ally, status)
        self.description = "On Reveal: If your opponent played a card here this turn, +4 power."

    def onReveal(self, locationlist):
        if self.ally:
            if len(self.location.preRevealEnemies) >0:
                self.onreveal_buff += 4
        else:
            if len(self.location.preRevealAllies) >0:
                self.onreveal_buff += 4

class RocketRacoon(Card):
    def __init__(self, ally, status):
        super().__init__(1, 1, "Rocket Racoon", ally, status)
        self.description = "On Reveal: If your opponent played a card here this turn, +4 power."

    def onReveal(self, locationlist):
        if self.ally:
            if len(self.location.preRevealEnemies) >0:
                self.onreveal_buff += 4
        else:
            if len(self.location.preRevealAllies) >0:
                self.onreveal_buff += 4

class Medusa(Card):
    def __init__(self, ally, status):
        super().__init__(2, 2, "Medusa", ally, status)
        self.description = "On Reveal: If this is at the middle location, +3 Power"
    
    def onReveal(self, locationlist):
        if self.location == locationlist["location2"]:
            self.onreveal_buff += 3

class Odin(Card):
    def __init__(self, ally, status):
        super().__init__(6, 8, "Odin", ally, status)
        self.description = "On Reveal: Repeat the On Reveal abilities of your other cards here"
    
    def onReveal(self, locationlist):
        if self.ally:
            cur = self.location.allies
        else:
            cur = self.location.enemies
        for unit in cur:
            if unit != self:
                unit.onReveal(locationlist)

class Wolfsbane(Card):
    def __init__(self, ally, status):
        super().__init__(3, 1, "Wolfsbane", ally, status)
        self.description = "On Reveal: +2 Power for each other card you have here"
    
    def onReveal(self, locationlist):
        if self.ally: 
            self.onreveal_buff += 2*(len(self.location.allies))
        else:
            self.onreveal_buff += 2*(len(self.location.enemies))

class WhiteTiger(Card):
    def __init__(self, ally, status):
        super().__init__(5, 1, "White Tiger", ally, status)
        self.description = "On Reveal: Add a 8-Power Tiger to another location."
    
    def onReveal(self, locationlist):
        possible = []
        if self.ally:
            for loc in locationlist.values():
                if loc != self.location and len(loc.allies) <4:
                        possible.append(loc)
        else:
            for loc in locationlist.values():
                if loc != self.location and len(loc.enemies) <4:
                        possible.append[loc]
        if len(possible) > 0:
            loc = random.choice(possible)
            loc.allies.append(Card(5, 8, "Tiger", self.ally, self.status))
        else:
            print("No possible locations")

class Ironman(Card):
    def __init__(self, ally, status):
        super().__init__(5, 0, "Ironman", ally, status)
        self.description = "Ongoing = Your total Power is doubled here."
        self.has_ongoing_late = True
    
    def ongoing(self, locationlist):
        if self.ally:
            self.location.alliesPowerWithBuff = self.location.alliesPowerWithBuff * 2
        else:
            self.location.enemiesPowerWithBuff = self.location.enemiesPowerWithBuff * 2

class CaptainAmerica(Card):
    def __init__(self, ally, status):
        super().__init__(3, 3, "Captain America", ally, status)
        self.description = "Ongoing: Your other Ongoing cards here have +2 Power."
        self.has_ongoing = True

    def ongoing(self, card):
        card.ongoing_buff += 1
    
    def applyOngoing(self,locationlist):
        if self.ally:
            for unit in self.location.allies:
                if unit != self:
                    unit.ongoing_to_apply.append(self)
        else:
            for unit in self.location.enemies:
                if unit != self:
                    unit.ongoing_to_apply.append(self)

class Armor(Card): 
    def __init__(self, ally, status):
        super().__init__(2, 3, "Armor", ally, status)
        self.description= "Ongoing: Cards can't be destroyed here"
        self.has_ongoing = True
    
    def applyOngoing(self, locationlist):
        self.location.ongoing_to_apply.append(self)
    
    def ongoing(self, location):
        location.can_destroy = False

class Kazan(Card):
    def __init__(self, ally, status):
        super().__init__(4, 4, "Kazan", ally, status)
        self.description = "Ongoing: Your 1-cost cards have +1 Power."
        self.has_ongoing = True

    def ongoing(self, card):
        card.ongoing_buff += 1
    
    def applyOngoing(self, locationlist):
        if self.ally:
            for unit in locationlist["location1"].allies + locationlist["location2"].allies + locationlist["location3"].allies:
                if unit.cost == 1:
                    unit.ongoing_to_apply.append(self)
        else:
            for unit in locationlist["location1"].enemies + locationlist["location2"].enemies + locationlist["location3"].enemies:
                if unit.cost == 1:
                    unit.ongoing_to_apply.append(self)
class Heimdall(Card):
    def __init__(self, ally, status):
        super().__init__(1, 10, "Heimdall", ally, status)
        self.description = "On Reveal: Move your other cards one location to the left"

    def onReveal(self, locationlist):
        print("Heimdall!")
        if self.ally:
            for unit in locationlist["location1"].allies + locationlist["location2"].allies + locationlist["location3"].allies:
                if unit != self:
                    newloc= unit.location.returnRightOrLeftLocation(-1)
                    if newloc != None:
                        unit.move(unit.location.returnRightOrLeftLocation(-1))
        else:
            for unit in locationlist["location1"].enemies + locationlist["location2"].enemies + locationlist["location3"].enemies:
                if unit != self:
                    newloc= unit.location.returnRightOrLeftLocation(-1)
                    if newloc != None:
                        unit.move(unit.location.returnRightOrLeftLocation(-1))

class MultipleMan(Card):
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
    
class HandBuffTest(Card):
    def __init__(self, ally, status):
        super().__init__(0, 0, "HandBuffTest", ally, status)
        self.description = "On Reveal: Give +3 power to every card in your hand"
    
    def onReveal(self, locationlist):
        if self.ally:
            for unit in self.status["allyhand"]:
                unit.onreveal_buff += 3
        else:
            for unit in self.status["enemyhand"]:
                unit.onreveal_buff += 3

class OldCaptainAmerica(Card):
    def __init__(self, ally, status):
        super().__init__(3, 4, "Old Captain America", ally, status)
        self.description = "Ongoing: Your other cards here have +1 Power."
        self.has_ongoing = True
        self.has_ongoing_buffpower = True

    def ongoing(self, card):
        card.ongoing_buff += 1
    
    def applyOngoing(self, locationlist):
        if self.ally:
            for unit in self.location.allies:
                if unit != self:
                    unit.ongoing_to_apply.append(self)
        else:
            for unit in self.location.enemies:
                if unit != self:
                    unit.ongoing_to_apply.append(self)

class Klaw(Card):
    def __init__(self, ally, status):
        super().__init__(1, 4, "Klaw", ally, status)
        self.description = "Ongoing: The location to the right has +7 Power."
        self.has_ongoing = True

    def ongoing(self, location):
        if self.ally:
            location.allies_power_buff_sum += 7
        else:
            location.enemies_power_buff_sum += 7
    
    def applyOngoing(self, locationlist):
        location = self.location.returnRightOrLeftLocation(1)
        if location != None:
            location.ongoing_to_apply.append(self)

class MrFantastic(Card):
    def __init__(self, ally, status):
        super().__init__(3, 2, "Mr Fantastic", ally, status)
        self.description = "Ongoing: The location to the left and right have +2 Power."
        self.has_ongoing = True
    
    def applyOngoing(self, locationlist):
        location = self.location.returnRightOrLeftLocation(1)
        if location != None:
            location.ongoing_to_apply.append(self)
        location = self.location.returnRightOrLeftLocation(-1)
        if location != None:
            location.ongoing_to_apply.append(self)
    
    def ongoing(self, location):
        if self.ally:
            location.allies_power_buff_sum += 2
        else:
            location.enemies_power_buff_sum += 2

class Onslaught(Card):
    def __init__(self, ally, status):
        super().__init__(6, 7, "Onslaught", ally, status)
        self.description = "Ongoing: Your Ongoings here are doubled."
        self.has_ongoing = True
        self.onslaught = True

class Antman(Card):
    def __init__(self, ally, status):
        super().__init__(1, 1, "Antman", ally, status)
        self.description = "Ongoing: If your side of this location is full, +4 power."
        self.has_ongoing = True
    
    def applyOngoing(self, locationlist):
        if self.ally:
            if len(self.location.allies) == 4:
                self.ongoing_to_apply.append(self)
        else:
            if len(self.location.enemies) == 4:
                self.ongoing_to_apply.append(self)
    
    def ongoing(self, locationlist):
        self.ongoing_buff += 4

class Lizard(Card):
    def __init__(self, ally, status):
        super().__init__(2, 5, "Lizard", ally, status)
        self.description = "Ongoing: -4 power if your opponent has 4 cards here."
        self.has_ongoing = True

    def applyOngoing(self, locationlist):
        if self.ally:
            if len(self.location.enemies) == 4:
                self.ongoing_to_apply.append(self)
        else:
            if len(self.location.allies) == 4:
                self.ongoing_to_apply.append(self)
    
    def ongoing(self, locationlist):
        self.ongoing_buff -= 4

class Punisher(Card):
    def __init__(self, ally, status):
        super().__init__(3, 3, "Punisher", ally, status)
        self.description = "Ongoing: +1 power for each enemy card here."
        self.has_ongoing = True

    def applyOngoing(self, locationlist):
        self.ongoing_to_apply.append(self)
    
    def ongoing(self, locationlist):
        if self.ally:
            self.ongoing_buff += len(self.location.enemies)
        else:
            self.ongoing_buff += len(self.location.allies)

class SpiderWoman(Card):
    def __init__(self, ally, status):
        super().__init__(5, 8, "Spider-Woman", ally, status)
        self.description = "On Reveal: Afflict all enemy cards here with -1 power."
    
    def onReveal(self, locationlist):
        if self.ally:
            for unit in self.location.enemies:
                unit.onreveal_buff -= 1
        else:
            for unit in self.location.allies:
                unit.onreveal_buff -= 1

class DevilDinosaur(Card):
    def __init__(self, ally, status):
        super().__init__(5, 3, "Devil Dinosaur", ally, status)
        self.description = "Ongoing: +2 Power for each card in your hand."
        self.has_ongoing = True
    
    def applyOngoing(self, locationlist):
        self.ongoing_to_apply.append(self)
    
    def ongoing(self, locationlist):
        if self.ally:
            self.ongoing_buff += 2*len(self.status["allyhand"])
        else:
            self.ongoing_buff += 2*len(self.status["enemyhand"])

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

class BlueMarvel(Card):
    def __init__(self, ally, status):
        super().__init__(5, 3, "Blue Marvel", ally, status)
        self.description = "Ongoing: Your other cards have +1 Power."
        self.has_ongoing = True
    
    def applyOngoing(self, locationlist):
        if self.ally:
            for unit in locationlist["location1"].allies + locationlist["location2"].allies + locationlist["location3"].allies:
                if unit != self:
                    unit.ongoing_to_apply.append(self)
        else:
            for unit in locationlist["location1"].enemies + locationlist["location2"].enemies + locationlist["location3"].enemies:
                if unit != self:
                    unit.ongoing_to_apply.append(self)
    
    def ongoing(self, card):
        card.ongoing_buff += 1

class Enchantress(Card):
    def __init__(self, ally, status):
        super().__init__(4, 6, "Enchantress", ally, status)
        self.description = "On Reveal: Remove the abilities from all Ongoing cards here"
    
    def onReveal(self, locationlist):
        if self.ally:
            for unit in self.location.enemies:
                unit.has_ongoing = False
        else:
            for unit in self.location.allies:
                unit.has_ongoing = False

class Namor(Card):
    def __init__(self, ally, status):
        super().__init__(4, 6, "Namor", ally, status)
        self.description = "+5 Power if this is your only card here."
        self.has_ongoing = True
    
    def applyOngoing(self, locationlist):
        if self.ally:
            if len(self.location.allies) == 1:
                self.ongoing_to_apply.append(self)
        else:
            if len(self.location.enemies) == 1:
                self.ongoing_to_apply.append(self)
    
    def ongoing(self, locationlist):
        self.ongoing_buff += 5

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
                
class Jubilee(Card):
    def __init__(self, ally, status):
        super().__init__(4, 1, "Jubilee", ally, status)
        self.description = "On Reveal: Add the top card of your deck to this location."
    
    def onReveal(self, locationlist):
        if self.ally and len(self.status["allydeck"]) > 0 and (len(self.location.allies) + len(self.location.preRevealAllies)) < 4:
            self.location.preRevealAllies.append(self.status["allydeck"].pop(0))
        elif not self.ally and len(self.status["enemydeck"]) > 0 and (len(self.location.enemies) + len(self.location.preRevealEnemies)) < 4:
            self.location.preRevealEnemies.append(self.status["enemydeck"].pop(0))
            
class Okoye(Card):
    def __init__(self, ally, status):
        super().__init__(2, 3, "Okoye", ally, status)
        self.description = "On Reveal: Give every card in your deck +1 Power."
    
    def onReveal(self, locationlist):
        if self.ally:
            for card in self.status["allydeck"]:
                card.onreveal_buff += 1
        else:
            for card in self.status["enemydeck"]:
                card.onreveal_buff += 1

class ScarletWitch(Card):
    def __init__(self, ally, status):
        super().__init__(2, 3, "Scarlet Witch", ally, status)
        self.description = "On Reveal: Replace this location with a new one."
    
    def onReveal(self, locationlist):
        self.location.changeLocation(self.location.randomLocation())

class Vulture(Card):
    def __init__(self, ally, status):
        super().__init__(3, 3, "Vulture", ally, status)
        self.description = "When this card moves, +6 Power."
    
    def onMove(self):
        self.onreveal_buff += 6
    
class Warpath(Card):
    def __init__(self, ally, status):
        super().__init__(4, 5, "Warpath", ally, status)
        self.description = "Ongoing: if any of your locations are empty, +5 Power."
        self.has_ongoing = True
    
    def applyOngoing(self, locationlist):
        if self.ally:
            if len(locationlist["location1"].allies) == 0 or len(locationlist["location2"].allies) == 0 or len(locationlist["location3"].allies) == 0:
                self.ongoing_to_apply.append(self)
        
        else:
            if len(locationlist["location1"].enemies) == 0 or len(locationlist["location2"].enemies) == 0 or len(locationlist["location3"].enemies) == 0:
                self.ongoing_to_apply.append(self)
    
    def ongoing(self, locationlist):
        self.ongoing_buff += 5

class WhiteQueen(Card):
    def __init__(self, ally, status):
        super().__init__(3, 4, "White Queen", ally, status)
        self.description= "On Reveal: Copy the card that costs the most from your opponent's hand into your hand."

    def onReveal(self, locationlist):
        if self.ally:
            max_cost = max(obj.cost for obj in self.status["enemyhand"])
            max_cost_items = [obj for obj in self.status["enemyhand"] if obj.cost == max_cost]
            self.status["allyhand"].append(copy.deepcopy(random.choice(max_cost_items)))
        else:
            max_cost = max(obj.cost for obj in self.status["allyhand"])
            max_cost_items = [obj for obj in self.status["allyhand"] if obj.cost == max_cost]
            self.status["enemyhand"].append(copy.deepcopy(random.choice(max_cost_items))) 

class Cosmo(Card):
    def __init__(self, ally, status):
        super().__init__(3, 3, "Cosmo", ally, status)
        self.description = "Ongoing: On Reveal abilities won't happen here"
        self.has_ongoing = True
    
    def applyOngoing(self, locationlist):
        self.location.ongoing_to_apply.append(self)
    
    def ongoing(self, location):
        location.on_reveal_number_allies, location.on_reveal_number_enemies = 0, 0

class EbonyMaw(Card):
    def __init__(self, ally, status):
        super().__init__(1, 7, "Ebony Maw", ally, status)
        self.description = "You can't play this after turn 3. Ongoing: You can't play cards here"
        self.has_ongoing = True
    
    def updateCard(self):
        super().updateCard()
        if self.status["turncounter"] >= 3:
            self.can_be_played = False
        
    def ongoing(self, location):
        if self.ally:
            location.can_play_cards_allies = False
        else:
            location.can_play_cards_enemies = False
    
    def applyOngoing(self, locationlist):
        self.location.ongoing_to_apply.append(self)

class ProfessorX(Card):
    def __init__(self, ally, status):
        super().__init__(5, 3, "Professor X", ally, status)
        self.description = "You can't play this after turn 3. Ongoing: You can't play cards here"
        self.has_ongoing = True
    
    def ongoing(self, location):
        location.can_play_cards_allies, location.can_play_cards_enemies = False, False
        location.can_destroy = False
    
    def applyOngoing(self, locationlist):
        self.location.ongoing_to_apply.append(self)

class ShangChi(Card):
    def __init__(self, ally, status):
        super().__init__(4, 3, "Shang-Chi", ally, status)
        self.description = "On Reveal: Destroy all enemy cards here with 10+ Power"
    
    def onReveal(self, locationlist):
        if self.ally:
            for card in self.location.enemies:
                if card.cur_power >= 10:
                    self.location.destroyCard(card)
        else:
            for card in self.location.allies:
                if card.cur_power >= 10:
                    self.location.destroyCard(card) 

class Nightcrawler(Card):
    def __init__(self, ally, status):
        super().__init__(1, 2, "Nightcrawler", ally, status)
        self.description = "You can move this card once"
        self.moves_number = 1

class Vision(Card):
    def __init__(self, ally, status):
        super().__init__(3, 5, "Vision", ally, status)
        self.description = "You can move this card every turn"
        self.moves_number = 100

class Spectrum(Card):
    def __init__(self, ally, status):
        super().__init__(6, 7, "Spectrum", ally, status)
        self.description = "On Reveal: Give your Ongoing cards +2 Power"
    
    def onReveal(self, locationlist):
        if self.ally:
            for card in locationlist["location1"].allies + locationlist["location2"].allies + locationlist["location3"].allies:
                if card.has_ongoing:
                    card.onreveal_buff += 2
        else:
            for card in locationlist["location1"].enemies + locationlist["location2"].enemies + locationlist["location3"].enemies:
                if card.has_ongoing:
                    card.onreveal_buff += 2

class SquirrelGirl(Card):
    def __init__(self, ally, status):
        super().__init__(1, 2, "Squirrel Girl", ally, status)
        self.description = "On Reveal: Add a 1-Power Squirrel to each other location"

    class Squirrel(Card):
        def __init__(self, ally, status):
            super().__init__(1, 1, "Squirrel", ally, status)
            self.description = "Squeak!"
        
    def onReveal(self, locationlist):
        if self.ally:
            for location in locationlist.values():
                if location != self.location and len(location.allies) < 4:
                    newSquirrel = self.Squirrel(self.ally, self.status)
                    location.allies.append(newSquirrel)
                    newSquirrel.location = location
        else:
            for location in locationlist.values():
                if location != self.location and len(location.enemies) < 4:
                    newSquirrel = self.Squirrel(self.ally, self.status)
                    location.enemies.append(newSquirrel)
                    newSquirrel.location = location
def StrongGuy(Card):
    def __init__(self, ally, status):
        super().__init__(3, 3, "Strong Guy", ally, status)
        self.description = "Ongoing: if your hand has 1 or fewer cards, +6 power"
        self.has_ongoing = True
    
    def ongoing(self, card):
        self.ongoing_buff += 6
    
    def applyOngoing(self, locationlist):
        if self.ally:
            if len(self.status["allyhand"]) <= 1:
                self.ongoing_to_apply.append(self)
        else:
            if len(self.status["enemyhand"]) <= 1:
                self.ongoing_to_apply += 6

class Cable(Card):
    def __init__(self, ally, status):
        super().__init__(2, 3, "Cable", ally, status)
        self.description = "On Reveal: Draw a card from the opponent's deck"
    
    def onReveal(self, locationlist):
        if self.ally:
            if len(self.status["enemydeck"]) != 0:
                self.status["allyhand"].append(self.status["enemydeck"][-1])
                self.status["enemydeck"].pop().ally = True
        else:
            if len(self.status["allydeck"]) != 0:
                self.status["enemyhand"].append(self.status["allydeck"][-1])
                self.status["allydeck"].pop().ally = False