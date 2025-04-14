from Cards.Card import Card
from Locations.Location import Location
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
        if self.ally and len(self.status["allydeck"])>0:
            self.status["allydeck"][-1].onreveal_buff += 2
        elif not self.ally and len(self.status["enemydeck"])>0:
            self.status["enemydeck"][-1].onreveal_buff += 2
        print("Increased power of the card on top of the deck by 2!")

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

class Death(Card):
    def __init__(self, ally, status):
        super().__init__(8, 12, "Death", ally, status)
        self.description = "Costs 1 less for each card that was destroyed this game"
    
    def updateCard(self,locationlist):
        super().updateCard(locationlist)
        self.cur_cost = 12 - len(self.status["alliesdestroyed"]) - len(self.status["enemiesdestroyed"])

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

class Groot(Card):
    def __init__(self, ally, status):
        super().__init__(3, 3, "Groot", ally, status)
        self.description = "On Reveal: If your opponent played a card here this turn, +4 power."

    def onReveal(self, locationlist):
        if self.ally:
            if len(self.location.preRevealEnemies) >0:
                self.onreveal_buff += 4
        else:
            if len(self.location.preRevealAllies) >0:
                self.onreveal_buff += 4

class Gamora(Card):
    def __init__(self, ally, status):
        super().__init__(5, 8, "Gamora", ally, status)
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
        self.has_ongoing = True
    
    def ongoing(self, locationlist):
        if self.ally:
            self.location.allies_power_buff_mult = self.location.allies_power_buff_mult * 2
        else:
            self.location.enemies_power_buff_mult = self.location.enemies_power_buff_mult * 2
    
    def applyOngoing(self, locationlist):
        self.location.ongoing_to_apply.append(self)

class CaptainAmerica(Card):
    def __init__(self, ally, status):
        super().__init__(3, 3, "Captain America", ally, status)
        self.description = "Ongoing: Your other Ongoing cards here have +2 Power."
        self.has_ongoing = True

    def ongoing(self, card):
        card.ongoing_buff += 2
    
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
                if unit.base_cost == 1:
                    unit.ongoing_to_apply.append(self)
        else:
            for unit in locationlist["location1"].enemies + locationlist["location2"].enemies + locationlist["location3"].enemies:
                if unit.base_cost == 1:
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
    
    def applyOngoing(self, locationlist):
        if self.ally:
            for unit in self.location.allies:
                if unit != self and not unit.onslaught:
                    unit.applyOngoing(self.locationlist)
        else:
            for unit in self.location.enemies:
                if unit != self and not unit.onslaught:
                    unit.applyOngoing(locationlist)

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
            max_cost = max(obj.cur_cost for obj in self.status["enemyhand"])
            max_cost_items = [obj for obj in self.status["enemyhand"] if obj.cur_cost == max_cost]
            self.status["allyhand"].append(copy.deepcopy(random.choice(max_cost_items)))
        else:
            max_cost = max(obj.cur_cost for obj in self.status["allyhand"])
            max_cost_items = [obj for obj in self.status["allyhand"] if obj.cur_cost == max_cost]
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
    
    def updateCard(self,locationlist):
        super().updateCard(locationlist)
        if self.status["turncounter"] > 3:
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

class Storm(Card):
    def __init__(self, ally, status):
        super().__init__(4, 5, "Storm", ally, status)
        self.description = "On Reveal: Flood this location. Next turn is the last turn cards can be played here"
    class Flooding(Location):
        def __init__(self, number, status, locationlist):
            super().__init__(number, status, locationlist)
            self.name = "Flooding"
            self.description = "This is the last turn cards can be played here"
            self.counter = 1
    
        def startOfTurn(self):
            super().startOfTurn()
            self.counter -=1
        
        class Flooded(Location):
            def __init__(self, number, status, locationlist):
                super().__init__(number, status, locationlist)
                self.name = "Flooded"
                self.description = "Cards can't be played here"
                self.can_be_played = False

        def endOfTurn(self):
            super().endOfTurn()
            if self.counter == 0:
                self.changeLocation(self.Flooded(self.locationNum, self.status, self.locationlist))
    def onReveal(self, locationlist):
        self.location.changeLocation(self.Flooding(0, self.status,locationlist))

class MisterSinister(Card):
    def __init__(self, ally, status):
        super().__init__(2, 2, "Mister Sinister", ally, status)
        self.description = "On Reveal: Add a Sinister Clone here with the same power"

    class SinisterClone(Card):
        def __init__(self, ally, power, status):
            super().__init__(2, power, "Sinister Clone", ally, status)
            self.description = "Clone of Mister Sinister"

    def onReveal(self, locationlist):
        if self.ally and len(self.location.allies) < 4:
            newSinisterClone = self.SinisterClone(self.ally, self.cur_power, self.status)
            self.location.allies.append(newSinisterClone)
            newSinisterClone.location = self.location
        elif not self.ally and len(self.location.enemies) < 4:
            newSinisterClone = self.SinisterClone(self.ally, self.cur_power, self.status)
            self.location.enemies.append(newSinisterClone)
            newSinisterClone.location = self.location

class Kraven(Card):
    def __init__(self, ally, status):
        super().__init__(2, 3, "Kraven", ally, status)
        self.description = "When a card moves here, +2 Power"
    
    def onCardBeingMoved(self,card):
        if card.location == self.location:
            self.onreveal_buff += 2

class Nakia(Card):
    def __init__(self, ally, status):
        super().__init__(3, 3, "Nakia", ally, status)
        self.description = "On Reveal: Give +1 power to all cards in your hand"
    
    def onReveal(self, locationlist):
        if self.ally:
            for card in self.status["allyhand"]:
                card.onreveal_buff += 1
        else:
            for card in self.status["enemyhand"]:
                card.onreveal_buff += 1

class Morph(Card):
    def __init__(self, ally, status):
        super().__init__(3, 0, "Morph", ally, status)
        self.description = "On Reveal: Become a copy of a card in your opponent's hand"

    def onReveal(self, locationlist):
        if self.ally:
            if len(self.status["enemyhand"]) != 0:
                self.location.preRevealAllies.remove(self)
                morphInto = copy.deepcopy(random.choice(self.status["enemyhand"]))
                self.location.allies.append(morphInto)
                morphInto.location = self.location
                morphInto.ally = True
                morphInto.onReveal(locationlist)
        else:
            if len(self.status["allyhand"]) != 0:
                self.location.PreRevealEnemies.remove(self)
                morphInto = copy.deepcopy(random.choice(self.status["allyhand"]))
                self.location.enemies.append(morphInto)
                morphInto.location = self.location
                morphInto.ally = False
                morphInto.onReveal(locationlist)

class Blade(Card):
    def __init__(self, ally, status):
        super().__init__(1, 3, "Blade", ally, status)
        self.description = "On Reveal: Discard the leftmost card in your hand"
    
    def onReveal(self, locationlist):
        if self.ally:
            self.status["allyhand"][-1].discard()
        else:
            self.status["enemyhand"][-1].discard()

class Morbius(Card):
    def __init__(self, ally, status):
        super().__init__(2, 0, "Morbius", ally, status)
        self.description = "Ongoing: +2 Power for each card you discarded this game"
        self.has_ongoing = True
    
    def applyOngoing(self, locationlist):
        self.ongoing_to_apply.append(self)
    
    def ongoing(self, locationlist):
        if self.ally:
            self.ongoing_buff += 2*len(self.status["alliesdiscarded"])
        else:
            self.ongoing_buff += 2*len(self.status["enemiesdiscarded"])

class Swarm(Card):
    def __init__(self, ally, status):
        super().__init__(2, 3, "Swarm", ally, status)
        self.description = "When discarded, add 2 copies here that cost 0"
    
    def whenDiscarded(self):
        if self.ally:
            self.status["allyhand"].append(self.createCopy())
            self.status["allyhand"].append(self.createCopy())
        else:
            self.status["enemyhand"].append(self.createCopy())
            self.status["enemyhand"].append(self.createCopy())
    
    def createCopy(self):
        zerocostcopy = Swarm(self.ally, self.status)
        zerocostcopy.cost = 0
        zerocostcopy.base_power = self.base_power
        zerocostcopy.onreveal_buff = self.onreveal_buff
        zerocostcopy.was_created = True
        return zerocostcopy

class Modok(Card):
    def __init__(self, ally, status):
        super().__init__(5, 7, "Modok", ally, status)
        self.description = "On Reveal: Discard all cards in your hand"
    
    def onReveal(self, locationlist):
        if self.ally:
            toDiscard = copy.copy(self.status["allyhand"])
            for card in toDiscard:
                card.discard()
        else:
            toDiscard = copy.copy(self.status["enemyhand"])
            for card in toDiscard:
                card.discard()

class Apocalypse(Card):
    def __init__(self, ally, status):
        super().__init__(6, 7, "Apocalypse", ally, status)
        self.description = "When discarded, put it back with +4 power"
    
    def whenDiscarded(self):
        if self.ally:
            self.status["allyhand"].append(self)
            self.onreveal_buff += 4
        else:
            self.status["enemyhand"].append(self)
            self.onreveal_buff += 4

class Angela(Card):
    def __init__(self, ally, status):
        super().__init__(2, 3, "Angela", ally, status)
        self.description = "After you play a card here, +1 Power"
    
    def onCardBeingPlayed(self, card):
        print("Angela!")
        if card.ally == self.ally and card.location == self.location and card != self:
            self.onreveal_buff += 1

class Bishop(Card):
    def __init__(self, ally, status):
        super().__init__(3, 2, "Bishop", ally, status)
        self.description = "After you play a card, this gains +1 Power"
    
    def onCardBeingPlayed(self, card):
        if card.ally == self.ally and card != self:
            self.onreveal_buff += 1

class LadySif(Card):
    def __init__(self, ally, status):
        super().__init__(3, 5, "Lady Sif", ally, status)
        self.description = "On Reveal: Discard the highest cost card in your hand"
    
    def onReveal(self, locationlist):
        if self.ally:
            handToCheck = self.status["allyhand"]
        else:
            handToCheck = self.status["enemyhand"]
        
        highestCost = 0
        highestCostCard = []
        for card in handToCheck:
            if card.cur_cost == highestCost:
                highestCostCard.append(card)
            elif card.cur_cost > highestCost:
                highestCost = card.cur_cost
                highestCostCard = [card]
        
        random.choice(highestCostCard).discard()

class ColeenWing(Card):
    def __init__(self, ally, status):
        super().__init__(2, 4, "Coleen Wing", ally, status)
        self.description = "On Reveal: Discard the lowest cost card in your hand"
    
    def onReveal(self, locationlist):
        if self.ally:
            handToCheck = self.status["allyhand"]
        else:
            handToCheck = self.status["enemyhand"]
        
        lowestCost = 100
        lowestCostCard = []
        for card in handToCheck:
            if card.cur_cost == lowestCost:
                lowestCostCard.append(card)
            if card.cur_cost < lowestCost:
                lowestCost = card.cur_cost
                lowestCostCard = [card]
        
        random.choice(lowestCostCard).discard()

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
    
class Killmonger(Card):
    def __init__(self, ally, status):
        super().__init__(3, 3, "Killmonger", ally, status)
        self.description = "On Reveal: Destroy ALL 1-cost cards"
    
    def onReveal(self, locationlist):
        for location in locationlist.values():
            for card in location.allies + location.enemies:
                if card.base_cost == 1:
                    location.destroyCard(card)

class Nova(Card):
    def __init__(self, ally, status):
        super().__init__(1, 1, "Nova", ally, status)
        self.description = "When this card is destroyed, +1 Power to all allies"
    
    def whenDestroyed(self, locationlist):
        
        for location in locationlist.values():
            if self.ally:
                for card in location.allies:
                    card.onreveal_buff += 1
            else:
                for card in location.enemies:
                    card.onreveal_buff += 1

class JessicaJones(Card):
    def __init__(self, ally, status):
        super().__init__(4, 5, "Jessica Jones", ally, status)
        self.description = "On Reveal: If you don't play a card at this location next turn, +5 Power"
        self.turnToCheck = 0
        self.onRevealNum = 0
    
    def onReveal(self, locationlist):
        self.onRevealNum += 1
        self.turnToCheck = self.status["turncounter"] + 1
    
    def endOfTurn(self):
        check = True
        if self.status["turncounter"] == self.turnToCheck and self.onRevealNum != 0:
            for cardPlayed in self.status["cardsplayed"]:
                if cardPlayed[1] == self.turnToCheck and cardPlayed[2] == self.locationNumToCheck and cardPlayed[0].ally == self.ally:
                    print("You played a card here this turn")
                    check = False
                    break
            if check:
                print("Buffing Jessica Jones!")
                self.onreveal_buff += 5*self.onRevealNum

class Ironheart(Card):
    def __init__(self, ally, status):
        super().__init__(3, 0, "Ironheart", ally, status)
        self.description = "On Reveal: Give 3 of your other cards +2 Power"
    
    def onReveal(self, locationlist):
        alreadyApplied = []
        if self.ally:
            for card in locationlist["location1"].allies + locationlist["location2"].allies + locationlist["location3"].allies:
                if card != self and len(alreadyApplied) <3:
                    alreadyApplied.append(card)
                    card.onreveal_buff += 2
        else:
            for card in locationlist["location1"].enemies + locationlist["location2"].enemies + locationlist["location3"].enemies:
                if card != self and len(alreadyApplied) <3:
                    alreadyApplied.append(card)
                    card.onreveal_buff += 2

class Hawkeye(Card):
    def __init__(self, ally, status):
        super().__init__(1, 1, "Hawkeye", ally, status)
        self.description = "On Reveal: If you play a card at this location next turn, +3 Power"
        self.turnToCheck = 0
        self.onRevealNum = 0
    
    def onReveal(self, locationlist):
        self.onRevealNum += 1
        self.turnToCheck = self.status["turncounter"] + 1
        self.locationNumToCheck = self.location.locationNum
    
    def endOfTurn(self):
        check = False
        if self.status["turncounter"] == self.turnToCheck and self.onRevealNum != 0:
            for cardPlayed in self.status["cardsplayed"]:
                if cardPlayed[1] == self.turnToCheck and cardPlayed[2] == self.locationNumToCheck and cardPlayed[0].ally == self.ally:
                    check = True
                    break
            if check:
                print("Buffing Hawkeye!")
                self.onreveal_buff += 3*self.onRevealNum

class Forge(Card):
    def __init__(self, ally, status):
        super().__init__(2, 2, "Forge", ally, status)
        self.description = "On Reveal: Give the next card you play +2 Power"
    
    def onReveal(self, locationlist):
        self.status["onnextcardbeingplayed"].append(self)
    
    def nextCardBuff(self, card):
        if card.ally == self.ally and card != self:
            card.onreveal_buff += 2
            self.status["onnextcardbeingplayed"].remove(self)

class Deathlok(Card):
    def __init__(self, ally, status):
        super().__init__(3, 5, "Deathlok", ally, status)
        self.description = "On Reveal: Destroy your other cards here"
    
    def onReveal(self, locationlist):
        if self.ally:
            for card in self.location.allies:
                if card != self:
                    self.location.destroyCard(card)
        else:
            for card in self.location.enemies:
                if card != self:
                    self.location.destroyCard(card)

class Mantis(Card):
    def __init__(self, ally, status):
        super().__init__(1, 2, "Mantis", ally, status)
        self.description = "On Reveal: If your opponent played any cards here this turn, copy one of them into your hand."

    def onReveal(self, locationlist):
        if self.ally:
            if len(self.location.preRevealEnemies) >0:
                self.status["allyhand"].append(copy.deepcopy(random.choice(self.location.preRevealEnemies)))
        else:
            if len(self.location.preRevealAllies) >0:
                self.status["enemyhand"].append(copy.deepcopy(random.choice(self.location.preRevealAllies)))

class IronFist(Card):
    def __init__(self, ally, status):
        super().__init__(1, 2, "Iron Fist", ally, status)
        self.description = "On Reveal: After you play your next card, move it one location to the left."
    
    def onReveal(self, locationlist):
        self.status["onnextcardbeingplayed"].append(self)
    
    def nextCardBuff(self, card):
        if card.ally == self.ally and card != self:
            print("Here for iron fist")
            self.status["onnextcardbeingplayed"].remove(self)
            newloc= card.location.returnRightOrLeftLocation(-1)
            if newloc != None:
                card.move(newloc)

class Uatu(Card):
    def __init__(self, ally, status):
        super().__init__(1, 2, "Uatu the Watcher", ally, status)
        self.description = "Game start: You can see the unrevealed locations"
    
    def startOfGame(self, locationlist):
        self.activate_in_deck = True
    
    def updateCard(self, locationlist):
        super().updateCard(locationlist)
        """Reveal the unrevealed locations."""
        print("Uatu is telling you that:")
        for location in locationlist.values():
            if location.temporary:
                print(f"Location {location.locationNum} will turn into: {location.newLoc.name}")

class SwordMaster(Card):
    def __init__(self, ally, status):
        super().__init__(3, 6, "Sword Master", ally, status)
        self.description = "On Reveal: Discard an odd-costed card from your hand."
    
    def onReveal(self, locationlist):
        toChoose = []
        if self.ally:
            for card in self.status["allyhand"]:
                if card.cur_cost % 2 == 1:
                    toChoose.append(card)
        else:
            for card in self.status["enemyhand"]:
                if card.cur_cost % 2 == 1:
                    toChoose.append(card)
        if len(toChoose) > 0:
            random.choice(toChoose).discard()

class Carnage(Card):
    def __init__(self, ally, status):
        super().__init__(2, 2, "Carnage", ally, status)
        self.description = "On Reveal: Destroy all your cards here. +2 Power for each destroyed"
    
    def onReveal(self, locationlist):
        cardsToDestroy = []
        if self.ally:
            for card in self.location.allies:
                if card != self:
                    cardsToDestroy.append(card)
        else:
            for card in self.location.enemies:
                if card != self:
                    cardsToDestroy.append(card)
        for card in cardsToDestroy:
                self.location.destroyCard(card)
                self.onreveal_buff += 2

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

class Moongirl(Card):
    def __init__(self, ally, status):
        super().__init__(4, 5, "Moongirl", ally, status)
        self.description = "On Reveal: Duplicate your hand."
    
    def onReveal(self, locationlist):
        temparray = []
        if self.ally:
            for card in self.status["allyhand"]:
                temparray.append(copy.deepcopy(card))
            self.status["allyhand"]+= temparray
        else:
            for card in self.status["enemyhand"]:
                temparray.append(copy.deepcopy(card))
            self.status["enemyhand"]+= temparray

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

class Yondu(Card):
    def __init__(self, ally, status):
        super().__init__(1, 2, "Yondu", ally, status)
        self.description = "On Reveal: Banish the card that costs the least in your opponent's deck."
    
    def onReveal(self, locationlist):
        if self.ally:
            if len(self.status["enemydeck"]) > 0:
                toBanish = min(self.status["enemydeck"], key=lambda x: x.cost)
                self.status["enemydeck"].remove(toBanish)
                print("Removed ", toBanish.name)
        else:
            if len(self.status["allydeck"]) > 0:
                toBanish = min(self.status["allydeck"], key=lambda x: x.cost)
                self.status["allydeck"].remove(toBanish)
                print("Removed ", toBanish.name)

class HulkBuster(Card):
    def __init__(self, ally, status):
        super().__init__(2, 3, "Hulk Buster", ally, status)
        self.description = "On Reveal: Merge with one of your cards here."
    
    def onReveal(self, locationlist):
        toMergeWith = []
        if self.ally:
            if len(self.location.allies) > 0:
                for card in self.location.allies:
                    if card != self:
                        toMergeWith.append(card)
        else:
            if len(self.location.enemies) > 0:
                for card in self.location.enemies:
                    if card != self:
                        toMergeWith.append(card)
        if len(toMergeWith) > 0:
            choice = random.choice(toMergeWith)
            self.merge(choice)
    
    def merge(self, card):
        card.onreveal_buff += self.cur_power
        if self.ally:
            self.location.allies.remove(self)
        else:
            self.location.enemies.remove(self)

class DoctorStrange(Card):
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
                card.move(self.location)

class BuckyBarnes(Card):
    def __init__(self, ally, status):
        super().__init__(2, 1, "Bucky Barnes", ally, status)
        self.description = "When this is destroyed, replace it with the Winter Soldier."
    
    class WinterSoldier(Card):
        def __init__(self, ally, status):
            super().__init__(2, 7, "Winter Soldier", ally, status)
            self.description = "It's time for me to face my past"
    
    def whenDestroyed(self, locationlist):
        if self.ally:
            locationlist["location1"].allies.append(self.WinterSoldier(self.ally, self.status))
        else:
            locationlist["location1"].enemies.append(self.WinterSoldier(self.ally, self.status))

class Scorpion(Card):
    def __init__(self, ally, status):
        super().__init__(2, 2, "Scorpion", ally, status)
        self.description = "On Reveal: Afflict cards in your opponent’s hand with -1 Power."
    
    def onReveal(self, locationlist):
        if self.ally:
            for card in self.status["enemyhand"]:
                card.onreveal_buff -= 1
        else:
            for card in self.status["allyhand"]:
                card.onreveal_buff -= 1

class Iceman(Card):
    def __init__(self, ally, status):
        super().__init__(1, 2, "Iceman", ally, status)
        self.description = "On Reveal: Give a card in your opponent’s hand +1 Cost. (maximum 6)"
    
    def onReveal(self, locationlist):
        toDebuff = []
        if self.ally:
            if len(self.status["enemyhand"]) > 0:
                for card in self.status["enemyhand"]:
                    if card.cost < 6:
                        toDebuff.append(card)
        else:
            if len(self.status["allyhand"]) > 0:
                for card in self.status["allyhand"]:
                    if card.cost < 6:
                        toDebuff.append(card)
        if len(toDebuff) > 0:
            choice = random.choice(toDebuff)
            choice.cost += 1
            print(f"{choice.name}", "now has a cost of", choice.cost)

class Sabretooth(Card):
    def __init__(self, ally, status):
        super().__init__(3, 5, "Sabretooth", ally, status)
        self.description = "When this is destroyed, return it to your hand. It costs 0."
    
    def whenDestroyed(self, locationlist):
        self.cost = 0
        if self.ally:
            self.status["allyhand"].append(self)
        else:
            self.status["enemyhand"].append(self)

class Rhino(Card):
    def __init__(self, ally, status):
        super().__init__(3, 3, "Rhino", ally, status)
        self.description = "On Reveal: Ruin this location. (Remove its ability)"
    
    class Ruin(Location):
        def __init__(self, number, status, locationlist):
            super().__init__(number, status, locationlist)
            self.name = "Ruin"
            self.description = "No ability"
    
    def onReveal(self, locationlist):
        self.location.changeLocation(self.Ruin(self.location.locationNum, self.status, locationlist))

class Cloak(Card):
    def __init__(self, ally, status):
        super().__init__(2, 4, "Cloak", ally, status)
        self.description = "On Reveal: Next turn, both players can move cards to this location."
    
    def onReveal(self, locationlist):
        self.turnToCheck = self.status["turncounter"] + 1
        self.locationToMove = self.location
    
    def startOfTurn(self):
        if self.turnToCheck == self.status["turncounter"]:
            self.location.location_can_be_moved_to = True

class Infinaut(Card):
    def __init__(self, ally, status):
        super().__init__(6, 20, "The Infinaut", ally, status)
        self.description = "If you played a card last turn, you can't play this"
    
    def updateCard(self, locationlist):
        self.can_be_played = True
        for cards in self.status["cardsplayed"]:
            print(cards)
            if cards[0].ally == self.ally and cards[1] == self.status["turncounter"]-1:
                self.can_be_played = False
"""
Atm too complicated to include due to how the on reveal works and the card does not see use in the game
class Sandman(Card):
    def __init__(self, ally, status):
        super().__init__(1, 8, "Sandman", ally, status)
        self.description = "On Reveal: Next turn, cards cost 1 more, max 6"
        self.turnToCheck = 0
    
    def onReveal(self, locationlist):
        self.turnToCheck = self.status["turncounter"] + 1

    def updateCard(self, locationlist):
        if self.turnToCheck == self.status["turncounter"]:
            print("Sandman!")
            for card in self.status["allyhand"] + self.status["enemyhand"]:
                if card.cur_cost >= 6:
                    self.ongoing_to_apply.append(card)
    
    def ongoing(self, locationlist):
        self.cost_ongoing += 1
"""
class Colossus(Card):
    def __init__(self, ally, status):
        super().__init__(2, 3, "Colossus", ally, status)
        self.has_ongoing = True
        self.description = "Ongoing: This card can't be destroyed, moved or have it's power reduced"
        self.onreveal_to_check = 0
        self.ongoing_to_check = 0
    
    def applyOngoing(self, locationlist):
        self.ongoing_to_apply.append(self)
    
    def ongoing(self, locationlist):
        self.can_be_destroyed = False
        self.onreveal_buff = self.onreveal_to_check= max(self.onreveal_to_check, self.onreveal_buff)
        self.ongoing_buff = self.ongoing_to_check = max(self.ongoing_to_check, self.ongoing_buff)
    
    def move(self, location):
        if self.has_ongoing:
            print("Colossus can't be moved!")
        else:
            super().move(location)
        
