import random
from Card import Card
from Location import Location
location1 = Location(1)
location2= Location(2)
location3= Location(3)
exit = False
turnAlly = False
allyenergy, enemyenergy =1,1
turncounter = 1
maxturns = 6

def addTolocation(location, unit):
    if(len(location)<4):
        location.append(unit)
        return True
    else:
        print("Location full")
        return False

def checkWinner():
    alliesWin = 0
    enemiesWin = 0
    allypower1, allypower2, allypower3 = location1.alliesPower, location2.alliesPower, location3.alliesPower
    enemypower1, enemypower2, enemypower3 = location1.enemiesPower, location2.enemiesPower, location3.enemiesPower
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
    match loc_num:
        case 1:
            if(turnAlly):
                location1.addToAllies(unit)
            else:
                location1.addToEnemies(unit)
        case 2:
            if(turnAlly):
                location2.addToAllies(unit)
            else:
                location2.addToEnemies(unit)
        case 3:
            if(turnAlly):
                location3.addToAllies(unit)
            else:
                location3.addToEnemies(unit)
def undoActions(turnAlly, hand):
    loc1temp =location1.undoActions(turnAlly)
    loc2temp =location2.undoActions(turnAlly)
    loc3temp =location3.undoActions(turnAlly)
    print("temps:", loc1temp, loc2temp, loc3temp)
    hand += loc1temp + loc2temp + loc3temp

def boardStatus(): #ritorna una stringa che definisce lo stato di ogni location 
    str1 = "Location 1: " + location1.locationStatus(),""
    str2 = "Location 2:" + location2.locationStatus(),""
    str3 = "Location 3:", location3.locationStatus(),""
    return str1+str2+str3

def draw(hand,deck,num): #pesca un numero di carte dal deck 
    i=0
    while i<num:
        hand.append(deck[-1])
        del deck[-1]
        i+=1

def gameStart(): #genera deck casuali uguali per ogni player per ora e li mischia 
    allydeck, enemydeck = [],[]
    for i in range (1,20,1):
        randomcost = random.randint(0,6)
        randompower = random.randint(1,10)
        cardname = "Number " + str(i)
        curCard = Card(randomcost,randompower, cardname)
        allydeck.append(curCard)
        enemydeck.append(curCard)
    allyhand,enemyhand = [],[]
    random.shuffle(allydeck)
    random.shuffle(enemydeck)
    draw(allyhand,allydeck,3)
    draw(enemyhand,enemydeck,3)
    return allyhand,enemyhand, allydeck, enemydeck

def playerTurn(hand, deck, maxenergy, currentBoard):
    draw(hand,deck,1)
    playerpass = False
    turnenergy = maxenergy
    while not playerpass:
        print()
        print("Press 1 to check hand and current energy, 2 to add an unit to the board, 3 to pass, 4 to check board status, 5 to undo your actions")
        userInput = int(input("What do you want to do? "))
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
                inputUnit = int(input()) -1
                try:
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
                print(currentBoard)
            case 5:
                undoActions(turnAlly, hand)
            case _:
                print("Input error")
def endGame():
    print(boardStatus())
    winner = checkWinner()
    match winner:
        case "ally":
            print("Allies have won")
        case "enemy":
            print("Enemies have won")
        case "tie":
            print("Tie!") 

allyhand,enemyhand,allydeck, enemydeck = gameStart()
while turncounter<=maxturns:
    tempBoard = boardStatus()
    print("Turn ", turncounter,", player turn")
    print("")
    turnAlly = not turnAlly
    playerTurn(allyhand, allydeck, allyenergy, tempBoard)
    print("Turn ", turncounter,", enemy turn")
    turnAlly = not turnAlly
    playerTurn(enemyhand, enemydeck, enemyenergy, tempBoard)
    location1.revealCards(True), location2.revealCards(True), location3.revealCards(True)
    turncounter +=1
    allyenergy+=1
    enemyenergy+=1
endGame()
 
    