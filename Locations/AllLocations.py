from Locations.Location import Location
import random
import copy

class Wakanda(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Wakanda"
        self.description = "Cards here can't be destroyed"
        self.can_destroy_base = False

class BarWithNoName(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Bar with no name"
        self.description = "Whoever has the least Power here wins."

    def locationWinner(self):
        if self.alliesPower < self.enemiesPower:
            self.winning = "Ally"
        elif self.alliesPower > self.enemiesPower:
            self.winning = "Enemy"
        else:
            self.winning = "Tie"

class KamarTaj(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Kamar-Taj"
        self.description = "On reveal effects activate twice here."
        self.on_reveal_number_base = self.on_reveal_number_base * 2

class Limbo(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Limbo"
        self.description = "There is a turn 7 this game."
    def onRevealLocation(self):
        self.status["maxturns"] = 7
    def changeLocation(self, newLocation):
        super().changeLocation(newLocation)
        check = False
        map_keys = map(self.locationlist.get, self.locationlist)
        for key in map_keys:
            if key.name == "Limbo":
                check = True
        if not check:
            self.status["maxturns"] = 6

class OnslaughtCitadel(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Onslaught Citadel"
        self.description = "Ongoing effects here are doubled"
        self.ongoing_number_base = 2

class Asgard(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Asgard"
        self.description = "After turn 4, whoever is winning here draws 2 cards"
    
    def endOfTurn(self):
        super().endOfTurn()
        if self.status["turncounter"] == 4:
            if self.winning == "Ally":
                print("Allies drawing 2")
                for i in range(2):
                    if self.status["allydeck"] != []:
                        self.status["allyhand"].append(self.status["allydeck"].pop())
            elif self.winning == "Enemy":
                print("Enemies drawing 2")
                for i in range(2):
                    if self.status["enemydeck"] != []:
                        self.status["enemyhand"].append(self.status["enemydeck"].pop())
    
class CastleBlackstone(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Castle Blackstone"
        self.description = "The player winning here gets +1 energy each turn"
    
    def startOfTurn(self):
        super().startOfTurn()
        if self.winning == "Ally":
            self.status["tempenergyally"] += 1
        elif self.winning == "Enemy":
            self.status["tempenergyenemy"] += 1

class NewYork(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "New York"
        self.description = "On turn 5, you can move cards here"
    
    def startOfTurn(self):
        super().startOfTurn()
        if self.status["turncounter"] == 5:
            print("You can move cards here!!")
            self.location_can_be_moved_to = True

class HellfireClub(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Hellfire Club"
        self.description = "You can't play 1 cost cards here"
    
    def canCardBePlayed(self,unit):
        if unit.cost == 1:
            return False
        elif unit.can_be_played:
            return True
        else:
            return False

class Mojoworld(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Mojoworld"
        self.description = "Whoever has more cards here gets +100 Power"
    
    def applyOngoing(self, locationlist):
        self.ongoing_to_apply.append(self)
    
    def ongoing(self, location):
        if len(location.allies) > len(location.enemies):
            self.allies_power_buff_sum += 100
        elif len(location.allies) < len(location.enemies):
            self.enemies_power_buff_sum += 100

class ProjectPegasus(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Project Pegasus"
        self.description = "+5 energy this turn"
    
    def onRevealLocation(self):
        super().onRevealLocation()
        self.status["tempenergyally"] += 5
        self.status["tempenergyenemy"] += 5

class SanctumSanctorum(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Sanctum Sanctorum"
        self.description = "Cards can't be played here"
        self.can_play_cards_base = False

class SewerSystem(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Sewer System"
        self.description = "Cards here have -1 Power"
    
    def applyOngoing(self, location):
        for unit in self.allies + self.enemies:
            unit.ongoing_to_apply.append(self)
    
    def ongoing(self, unit):
        unit.ongoing_buff -= 1

class Necrosha(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Necrosha"
        self.description = "Cards here have -2 Power"
    
    def applyOngoing(self, location):
        for unit in self.allies + self.enemies:
            unit.ongoing_to_apply.append(self)
    
    def ongoing(self, unit):
        unit.ongoing_buff -= 2

class NegativeZone(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Negative Zone"
        self.description = "Cards here have -3 Power"
    
    def applyOngoing(self, location):
        for unit in self.allies + self.enemies:
            unit.ongoing_to_apply.append(self)
    
    def ongoing(self, unit):
        unit.ongoing_buff -= 3

class Nidavellir(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Nidavellir"
        self.description = "Cards here have +5 Power"
    
    def applyOngoing(self, location):
        for unit in self.allies + self.enemies:
            unit.ongoing_to_apply.append(self)
    
    def ongoing(self, unit):
        unit.ongoing_buff += 5


class Atlantis(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Atlantis"
        self.description = "If you only have one card here, it has +5 Power"

    def applyOngoing(self, location):
        if len(self.allies) == 1:
            self.allies[0].ongoing_to_apply.append(self)
        if len(self.enemies) == 1:
            self.enemies[0].ongoing_to_apply.append(self)
    
    def ongoing(self, card):
        card.ongoing_buff += 5

class CrownCity(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Crown City"
        self.description = "Whoever is winning here gets +4 Power to adjacent locations"
    
    def applyOngoing(self, location):
        try:
            self.returnRightOrLeftLocation(1).ongoing_to_apply.append(self)
        except:
            pass
        try:
            self.returnRightOrLeftLocation(-1).ongoing_to_apply.append(self)
        except:
            pass
    
    def ongoing(self, location):
        if self.winning == "Ally":
            location.allies_power_buff_sum += 4
        elif self.winning == "Enemy":
            location.enemies_power_buff_sum += 4
        
class CrimsonCosmos(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Crimson Cosmos"
        self.description = "Cards that cost 1,2 or 3 can't be played here"
    
    def canCardBePlayed(self,unit):
        if unit.cost == 1 or unit.cost == 2 or unit.cost == 3:
            return False
        elif unit.can_be_played:
            return True
        else:
            return False
class PlunderCastle(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Plunder Castle"
        self.description = "Only cards that cost 6 can be played here"
    
    def canCardBePlayed(self,unit):
        if unit.cost == 6 and unit.can_be_played:
            return True
        else:
            return False
        
class LakeHeldas(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Lake Heldas"
        self.description = "Cards that cost 1 have +2 Power here"
    
    def applyOngoing(self, location):
        for unit in self.allies + self.enemies:
            if unit.cost == 1:
                unit.ongoing_to_apply.append(self)
    
    def ongoing(self, unit):
        unit.ongoing_buff +=1

class Kyln(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Kyln"
        self.description = "You can't play cards here after turn 4."
    
    def canCardBePlayed(self,unit):
        if self.status["turncounter"] <= 4 and unit.can_be_played:
            return True
        else:
            return False

class Milano(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Milano"
        self.description = "Turn 5 is the only turn cards can be played here"
    
    def canCardBePlayed(self,unit):
        if self.status["turncounter"] == 5 and unit.can_be_played:
            return True
        else:
            return False

class Jotunheim(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Jotunheim"
        self.description = "After each turn, cards here lose 1 Power"
    
    def endOfTurn(self):
        super().endOfTurn()
        for unit in self.allies + self.enemies:
            unit.onreveal_buff -= 1