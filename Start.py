import random
allies_loc1,allies_loc2, allies_loc3 = [], [], []
enemies_loc1,enemies_loc2, enemies_loc3 = [], [], []
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
    allypower1, allypower2, allypower3 = countPower(allies_loc1), countPower(allies_loc2), countPower(allies_loc3)
    enemypower1, enemypower2, enemypower3 = countPower(enemies_loc1), countPower(enemies_loc2), countPower(enemies_loc3)
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
def countPower(location):
    power = 0
    for unit in location:
        power += unit
    return power

def addUnit(unit):
    loc_num = 0
    while(loc_num not in [1,2,3]):
        loc_num = int(input("Choose location: "))
    match loc_num:
        case 1:
            if(turnAlly):
                return addTolocation(allies_loc1, unit)
            else:
                return addTolocation(enemies_loc1, unit)
        case 2:
            if(turnAlly):
                return addTolocation(allies_loc2, unit)
            else:
                return addTolocation(enemies_loc2, unit)
        case 3:
            if(turnAlly):
                return addTolocation(allies_loc3, unit)
            else:
                return addTolocation(enemies_loc3, unit)

def boardStatus():
    print("Location 1:",allies_loc1, " vs ", enemies_loc1)
    print("Location 2:",allies_loc2, " vs ", enemies_loc2)
    print("Location 3:",allies_loc3, " vs ", enemies_loc3)
def draw(hand,deck,num):
    i=0
    while i<num:
        hand.append(deck[-1])
        del deck[-1]
        i+=1

def playerTurn(hand, maxenergy):
    playerpass = False
    turnenergy = maxenergy
    while not playerpass:
        print()
        print("Press 1 to check hand and current energy, 2 to add an unit to the board, 3 to pass, 4 to check board status")
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
                    print(i,": Power:", unit[0]," Cost: ", unit[1] )
                    i+=1
                inputUnit = int(input()) -1
                try:
                    if turnenergy<hand[inputUnit][1]:
                        print("Not enough energy")
                    else:
                        addUnit(hand[inputUnit][0])
                        turnenergy-=hand[inputUnit][1]
                        del hand[inputUnit]
                except:
                    print("Input error")
            case 3:
                playerpass = True
            case 4:
                boardStatus()
            case _:
                print("Input error")

allydeck = [[2,1],[3,2],[4,3],[6,4],[8,5],[9,6],[2,1],[3,2],[4,3],[6,4],[8,5],[9,6]]
enemydeck = [[2,1],[3,2],[4,3],[6,4],[8,5],[9,6],[2,1],[3,2],[4,3],[6,4],[8,5],[9,6]]
allyhand,enemyhand = [],[]
random.shuffle(allydeck)
random.shuffle(enemydeck)
draw(allyhand,allydeck,3)
draw(enemyhand,enemydeck,3)
while turncounter<=maxturns:
    draw(allyhand,allydeck,1)
    draw(enemyhand,enemydeck,1)
    print("Turn ", turncounter,", player turn")
    print("")
    turnAlly = not turnAlly
    playerTurn(allyhand, allyenergy)
    print("Turn ", turncounter,", enemy turn")
    turnAlly = not turnAlly
    playerTurn(enemyhand, enemyenergy)
    turncounter +=1
    allyenergy+=1
    enemyenergy+=1
winner = checkWinner()
match winner:
    case "ally":
        print("Allies have won")
    case "enemy":
        print("Enemies have won")
    case "tie":
        print("Tie!")    
    