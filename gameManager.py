import importlib
import random
import cards
import Locations
from Locations.Location import *

class GameState():
    def __init__(self):
        self.exit = False
        self.turnAlly = False
        self.allymaxenergy, self.enemymaxenergy =1,1
        self.turncounter = 1
        self.maxturns = 6
        self.game_end = False
        self.locationList = {"location1": 0,"location2": 0, "location3": 0}
        self.status = {"maxturns": self.maxturns,"allymaxenergy": self.allymaxenergy,
                "enemymaxenergy": self.enemymaxenergy, "allyenergy": 1,
                    "enemyenergy":1, "turncounter":self.turncounter,
                    "tempenergyally":0, "tempenergyenemy":0,
                    "allyhand":[], "enemyhand":[],
                    "allydeck":[], "enemydeck":[],
                    "alliesdestroyed":[], "enemiesdestroyed":[],
                    "alliesdiscarded":[], "enemiesdiscarded":[],
                    "allypriority": True,
                    "cubes":1, "tempcubes":1,
                    "allysnapped":False, "enemysnapped": False,
                    "cardsplayed": [], "onnextcardbeingplayed": [],
                    "allypass": False, "enemypass": False,
                    "endofturncounterally":0, "endofturncounterenemy":0,}
        self.passStatus = {
                'turnpassally': self.status['allypass'],  
                'turnpassenemy': self.status['enemypass'],
                'winner': "None",
                'retreatally': False,
                'retreatenemy': False  
            }
        self.locationList["location1"]=TemporaryLocation(1,self.status,self.locationList)
        self.locationList["location2"]= TemporaryLocation(2,self.status,self.locationList)
        self.locationList["location3"]= TemporaryLocation(3,self.status,self.locationList)
        

    def reset(self):
            self.exit = False
            self.turnAlly = False
            self.allymaxenergy, self.enemymaxenergy = 1, 1
            self.turncounter = 1
            self.maxturns = 6
            self.game_end = False
            self.locationList = {"location1": 0, "location2": 0, "location3": 0}
            self.status = {"maxturns": self.maxturns,"allymaxenergy":self.allymaxenergy,
                "enemymaxenergy": self.enemymaxenergy, "allyenergy": 1,
                    "enemyenergy":1, "turncounter":self.turncounter,
                    "tempenergyally":0, "tempenergyenemy":0,
                    "allyhand":[], "enemyhand":[],
                    "allydeck":[], "enemydeck":[],
                    "alliesdestroyed":[], "enemiesdestroyed":[],
                    "alliesdiscarded":[], "enemiesdiscarded":[],
                    "allypriority": True,
                    "cubes":1, "tempcubes":1,
                    "allysnapped":False, "enemysnapped": False,
                    "cardsplayed": [], "onnextcardbeingplayed": [],
                    "allypass": False, "enemypass": False,
                    "endofturncounterally":0, "endofturncounterenemy":0,}
            self.passStatus = {
                    'turnpassally': self.status['allypass'],  
                    'turnpassenemy': self.status['enemypass'],
                    'winner': "None"  
                }
            self.locationList["location1"] = TemporaryLocation(1, self.status, self.locationList)
            self.locationList["location2"] = TemporaryLocation(2, self.status, self.locationList)
            self.locationList["location3"] = TemporaryLocation(3, self.status, self.locationList)
            self.gameStart()
    def resolveTie(self):
        allypower = self.locationList["location1"].alliesPower + self.locationList["location2"].alliesPower + self.locationList["location3"].alliesPower
        enemypower = self.locationList["location1"].enemiesPower + self.locationList["location2"].enemiesPower + self.locationList["location3"].enemiesPower
        if allypower > enemypower:
            return "Ally"
        elif allypower < enemypower:
            return "Enemy"
        else:
            return "Tie"

    def checkWinner(self):
        self.locationList["location1"].locationWinner(), self.locationList["location2"].locationWinner(), self.locationList["location3"].locationWinner()
        results = [self.locationList["location1"].winning,self.locationList["location2"].winning,self.locationList["location3"].winning]
        allywin, enemywin = 0,0
        print(results)
        for string in results:
            if string == "Ally":
                allywin +=1
            elif string == "Enemy":
                enemywin +=1
        if allywin > enemywin:
            return "Ally"
        elif allywin < enemywin:
            return "Enemy"
        else:
            return self.resolveTie()


    def addUnit(self,unit,ally, locNum):
        selectedLoc = "location" + str(locNum)
        if(ally):
            was_added = self.locationList[selectedLoc].addToAllies(unit)
            if was_added:
                unit.playCard(self.locationList[selectedLoc])
            return was_added
        else:
            was_added = self.locationList[selectedLoc].addToEnemies(unit)
            unit.playCard(self.locationList[selectedLoc])
            if was_added:
                unit.playCard(self.locationList[selectedLoc])
            return was_added
    
    def undoActions(self, turnAlly, hand):
        loc1temp = self.locationList["location1"].undoActions(turnAlly)
        loc2temp = self.locationList["location2"].undoActions(turnAlly)
        loc3temp = self.locationList["location3"].undoActions(turnAlly)
        print("temps:", loc1temp, loc2temp, loc3temp)
        refund = 0
        for unit in loc1temp + loc2temp + loc3temp:
            refund += unit.cur_cost
        hand += loc1temp + loc2temp + loc3temp
        return refund

    def boardStatus(self): #ritorna una stringa che definisce lo stato di ogni location 
        print(self.locationList["location1"].name,"[", self.locationList["location1"].description, "]: ", self.locationList["location1"].locationStatus(),"")
        print(self.locationList["location2"].name,"[", self.locationList["location2"].description, "]: ", self.locationList["location2"].locationStatus(),"")
        print(self.locationList["location3"].name,"[", self.locationList["location3"].description, "]: ", self.locationList["location3"].locationStatus(),"")

    def draw(self,hand,deck,num): #pesca un numero di carte dal deck 
        i=0
        if deck == []:
            print("No more cards in the deck!")
        else:
            while i<num:
                hand.append(deck[-1])
                del deck[-1]
                i+=1

    def gameStart(self): #inserisci carte nel deck e pesca le carte
        self.status["allydeck"], self.status["enemydeck"] = [cards.Swordmaster(True, self.status),cards.Heimdall(True,self.status)],[cards.Scorpion(False, self.status),cards.Onslaught(False, self.status)]
        self.status["allydeck"].append(cards.Apocalypse(True,self.status))
        self.status["enemydeck"].append(cards.Infinaut(False,self.status))
        for i in range (1,5,1):
            curCard = cards.Swarm(True, self.status)
            self.status["allydeck"].append(curCard)
            curCard = cards.Agent13(False, self.status)
            self.status["enemydeck"].append(curCard)
            curCard = cards.Blade(True, self.status)
            self.status["allydeck"].append(curCard)
            curCard = cards.Captainamerica(False, self.status)
            self.status["enemydeck"].append(curCard)
        random.shuffle(self.status["allydeck"])
        random.shuffle(self.status["enemydeck"])
        self.draw(self.status["allyhand"],self.status["allydeck"],3)
        self.draw(self.status["enemyhand"],self.status["enemydeck"],3)
        for location in self.locationList.values():
            location.startOfTurn()

    def playerTurn(self, hand, deck,energy):
        self.draw(hand,deck,1)
        for location in self.locationList.values():
            location.updateGameState()
        playerpass = False
        turnenergy = energy
        while not playerpass:
            print()
            print("Press 1 to check hand and current energy,"
            " 2 to add an unit to the board,"
            " 3 to pass,"
            " 4 to check board status,"
            " 5 to undo your actions, "
            "6 to move a card, "
            "7 to retreat,"
            " 8 to SNAP!")
            check = True
            while check:
                try:
                    userInput = int(input("What do you want to do? "))
                    check= False
                except:
                    print("InputError")
            match userInput:
                case 1:
                    print("Energy left: ", turnenergy)
                    i=1
                    for unit in hand:
                        print(i,": ",unit.name, "Cost:", unit.cur_cost," Power: ", unit.cur_power, " Description:", unit.description)
                        i+=1
                case 2:
                    print("Energy left:", turnenergy)
                    print("Which unit would you like to add")
                    i=1
                    for unit in hand:
                        print(i,": ",unit.name, "Cost:", unit.cur_cost," Power: ", unit.cur_power, " Description:", unit.description)
                        i+=1
                    
                case 3:
                    playerpass = True
                    return turnenergy
                case 4:
                    self.boardStatus()
                case 5:
                    turnenergy += self.undoActions(self.turnAlly, hand)
                case 6:
                    print("Which card would you like to move?")
                    self.moveSelection(self.turnAlly)
                case 8:
                    if (self.turnAlly and not self.status["allysnapped"]) or (not self.turnAlly and not self.status["enemysnapped"]):
                        print("SNAP!")
                        self.snap(self.status, self.turnAlly)
                    else: print("You already snapped!")

                case _:
                    print("Input error")

    def moveSelection(self, card, location):
        for moves in card.location.cards_to_move:
            if moves[0] == card:
                print("You already moved that card")
                return "error"
        if location == card:
            print("You can't move the card to the same location")
        else:
            if card.moves_number > 0 or location.location_can_be_moved_to:
                if not location.checkIfLocationFull(card.ally):
                    card.location.cards_to_move.append([card, location])
                    return "success"
                else:
                    return "Location full"
            else:
                return "You can't move that card!"
    


    def snap(self, turnAlly):
        if (turnAlly and not self.status["allysnapped"]):
            self.status["allysnapped"] = True
            if not self.status["enemysnapped"]: self.status["tempcubes"] = 2
            else: self.status["cubes"], self.status["tempcubes"] = 4,4
        else:
            self.status["enemysnapped"] = True
            if not self.status["allysnapped"]: self.status["tempcubes"] = 2
            else: self.status["cubes"], self.status["tempcubes"] = 4,4

    def startOfTurn(self):
        self.locationList["location1"].startOfTurn()
        self.locationList["location2"].startOfTurn()
        self.locationList["location3"].startOfTurn()
        self.status["allyenergy"] = self.status["allymaxenergy"] + self.status["tempenergyally"]
        self.status["enemyenergy"] = self.status["enemymaxenergy"] + self.status["tempenergyenemy"]
        self.status["tempenergyally"], self.status["tempenergyenemy"] = 0,0
        winning = self.checkWinner()
        for card in self.locationList["location1"].allies + self.locationList["location2"].allies + self.locationList["location3"].allies + self.locationList["location1"].enemies + self.locationList["location2"].enemies + self.locationList["location3"].enemies:
            card.startOfTurn()
        match winning:
            case "Ally" | "Tie":
                self.status["allypriority"] = True
                print("Allies have priority")
            case "Enemy":
                self.status["allypriority"] = False
                print("Enemies have priority")
        for card in self.status["allyhand"] + self.status["allydeck"] + self.status ["enemyhand"] + self.status["enemydeck"]:
            card.updateCard(self.locationList)
        self.draw(self.status["allyhand"],self.status["allydeck"],1)
        self.draw(self.status["enemyhand"],self.status["enemydeck"],1)
    def announcer(self):
        match self.status["allypriority"]:
            case True:
                print("Revealing ally cards")
            case False:
                print("Revealing enemy cards")

    def endOfTurn(self):
        self.status["cubes"] = self.status["tempcubes"]
        self.announcer()
        self.locationList["location1"].startOfTurnMoves(), self.locationList["location2"].startOfTurnMoves(), self.locationList["location3"].startOfTurnMoves()
        self.locationList["location1"].revealCards(), self.locationList["location2"].revealCards(), self.locationList["location3"].revealCards()
        self.status["allypriority"] = not self.status["allypriority"]
        self.announcer()
        self.locationList["location1"].revealCards(), self.locationList["location2"].revealCards(), self.locationList["location3"].revealCards()
        print("End of turn!")
        self.locationList["location1"].endOfTurn(), self.locationList["location2"].endOfTurn(), self.locationList["location3"].endOfTurn()
        self.status["turncounter"] +=1
        self.status["allymaxenergy"]+=1
        self.status["enemymaxenergy"]+=1


    def endGame(self):
        self.boardStatus()
        winner = self.checkWinner()
        self.game_end = True
        match winner:
            case "Ally":
                print("Allies have won ", self.status["cubes"]*2)
                print("Enemies have lost ", self.status["cubes"]*2)
            case "Enemy":
                print("Allies have lost ", self.status["cubes"]*2)
                print("Enemies have won ", self.status["cubes"]*2)
            case "Tie":
                print("Tie!")

    def gaming(self):
        while self.status["turncounter"]<=self.status["maxturns"]:
            print("Turn ", self.status["turncounter"],", player turn")
            print("")
            self.startOfTurn(self.status)
            self.boardStatus()
            turnAlly = not turnAlly
            print("Turn ", self.status["turncounter"],", enemy turn")
            turnAlly = not turnAlly
            self.status["enemyenergy"]= self.playerTurn(self.status["enemyhand"], self.status["enemydeck"], self.status["enemyenergy"])
            self.endOfTurn()
        self.endGame()
    
    def turnEnd(self):
        self.endOfTurn()
    
    def retreat(allyOrEnemy):
        pass
