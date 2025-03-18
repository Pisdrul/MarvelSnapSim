import random
from Cards.Card import *
from Location import *

exit = False
turnAlly = False
allymaxenergy, enemymaxenergy =1,1
turncounter = 1
maxturns = 6
locationList = {"location1": 0,"location2": 0, "location3": 0}
status = {"maxturns": maxturns,"allymaxenergy":allymaxenergy, "enemymaxenergy": enemymaxenergy, "allyenergy": 1, "enemyenergy":1, "turncounter":turncounter, "allyhand":[], "enemyhand":[], "allydeck":[], "enemydeck":[]}
locationList["location1"]=Location(1,status,locationList)
locationList["location2"]= onRevealActivatesTwice(2,status,locationList)
locationList["location3"]= TestLocationEffects(3,status,locationList)



def checkWinner():
    alliesWin = 0
    enemiesWin = 0
    allypower1, allypower2, allypower3 = locationList["location1"].alliesPower, locationList["location2"].alliesPower, locationList["location3"].alliesPower
    enemypower1, enemypower2, enemypower3 = locationList["location1"].enemiesPower, locationList["location2"].enemiesPower, locationList["location3"].enemiesPower
    alliesWin, enemiesWin = locationWon(allypower1,enemypower1, alliesWin, enemiesWin)
    alliesWin, enemiesWin = locationWon(allypower2,enemypower2, alliesWin, enemiesWin)
    alliesWin, enemiesWin = locationWon(allypower3,enemypower3, alliesWin, enemiesWin)
    totalpowerally= allypower1+allypower2+allypower3
    totalpowerenemy = enemypower1+enemypower2+enemypower3
    if (alliesWin>enemiesWin or (alliesWin == enemiesWin and totalpowerally>totalpowerenemy)):
        return "ally"
    elif (alliesWin<enemiesWin or (alliesWin == enemiesWin and totalpowerally<totalpowerenemy)):
        return "enemy"
    else:
        return "tie"

def locationWon(ally,enemy,counterally,counterenemy):
    if ally > enemy:
        counterally+=1
    elif enemy > ally:
        counterenemy+=1
    return counterally, counterenemy


def addUnit(unit):
    loc_num = 0
    while(loc_num not in [1,2,3]):
        loc_num = int(input("Choose location: "))
    selectedLoc = "location"+str(loc_num)
    if(turnAlly):
        locationList[selectedLoc].addToAllies(unit)
        unit.playCard(locationList[selectedLoc])
    else:
        locationList[selectedLoc].addToEnemies(unit)
        unit.playCard(locationList[selectedLoc])
    
def undoActions(turnAlly, hand):
    loc1temp =locationList["location1"].undoActions(turnAlly)
    loc2temp =locationList["location2"].undoActions(turnAlly)
    loc3temp =locationList["location3"].undoActions(turnAlly)
    print("temps:", loc1temp, loc2temp, loc3temp)
    hand += loc1temp + loc2temp + loc3temp

def boardStatus(): #ritorna una stringa che definisce lo stato di ogni location 
    print(locationList["location1"].name,": ",locationList["location1"].locationStatus(),"")
    print(locationList["location2"].name,": ",locationList["location2"].locationStatus(),"")
    print(locationList["location3"].name,": ", locationList["location3"].locationStatus(),"")

def draw(hand,deck,num): #pesca un numero di carte dal deck 
    i=0
    if deck == []:
        print("No more cards in the deck!")
    else:
        while i<num:
            hand.append(deck[-1])
            del deck[-1]
            i+=1

def gameStart(): #genera deck casuali uguali per ogni player per ora e li mischia 
    status["allydeck"], status["enemydeck"] = [OngoingTest(1,1,"Test Ongoing", True, status),EndOfTurnTest(1,0,"Test End of turn",True, status)],[TestCard(1,1,"Testcardenemies", False, status),EndOfTurnTest(1,0,"Test End of turn",False, status)]
    status["allydeck"].append(Magik(True,status))
    for i in range (1,8,1):
        randomcost = random.randint(0,6)
        randompower = random.randint(1,10)
        cardname = "Number " + str(i)
        curCard = Card(randomcost,randompower, cardname, True, status)
        status["allydeck"].append(curCard)
        curCard = Card(randomcost,randompower, cardname, False, status)
        status["enemydeck"].append(curCard)
    random.shuffle(status["allydeck"])
    random.shuffle(status["enemydeck"])
    draw(status["allyhand"],status["allydeck"],3)
    draw(status["enemyhand"],status["enemydeck"],3)

def playerTurn(hand, deck,energy):
    draw(hand,deck,1)
    playerpass = False
    turnenergy = energy
    while not playerpass:
        print()
        print("Press 1 to check hand and current energy, 2 to add an unit to the board, 3 to pass, 4 to check board status, 5 to undo your actions")
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
                print(hand)
            case 2:
                print("Energy left:", turnenergy)
                print("Which unit would you like to add")
                i=1
                for unit in hand:
                    print(i,": ",unit.name, "Power:", unit.power," Cost: ", unit.cost )
                    i+=1
                try:
                    inputUnit = int(input()) -1
                    if turnenergy<hand[inputUnit].cost:
                        print("Not enough energy")
                    else:
                        addUnit(hand[inputUnit])
                        turnenergy-=hand[inputUnit].cost
                        del hand[inputUnit]
                except:
                    print("Input error")
            case 3:
                playerpass = True
            case 4:
                boardStatus()
            case 5:
                undoActions(turnAlly, hand)
            case _:
                print("Input error")

def startOfTurn():
    pass
def endOfTurn():
    locationList["location1"].revealCards(True), locationList["location2"].revealCards(True), locationList["location3"].revealCards(True)
    print("End of turn!")
    locationList["location1"].endOfTurn(), locationList["location2"].endOfTurn(), locationList["location3"].endOfTurn()


def endGame():
    boardStatus()
    winner = checkWinner()
    match winner:
        case "ally":
            print("Allies have won")
        case "enemy":
            print("Enemies have won")
        case "tie":
            print("Tie!") 

gameStart()
while status["turncounter"]<=status["maxturns"]:
    boardStatus()
    print("Turn ", status["turncounter"],", player turn")
    print("")
    startOfTurn()
    turnAlly = not turnAlly
    playerTurn(status["allyhand"], status["allydeck"], status["allyenergy"])
    print("Turn ", status["turncounter"],", enemy turn")
    turnAlly = not turnAlly
    playerTurn(status["enemyhand"], status["enemydeck"], status["enemyenergy"])
    endOfTurn()
    status["turncounter"] +=1
    status["allyenergy"]+=1
    status["enemyenergy"]+=1
endGame()
 
    