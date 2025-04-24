import cards
from flask import *
import importlib
import random
import cards
from Locations.AllLocations import *
from Locations.Location import *

exit = False
turnAlly = False
allymaxenergy, enemymaxenergy =1,1
turncounter = 1
maxturns = 6
locationList = {"location1": 0,"location2": 0, "location3": 0}
status = {"maxturns": maxturns,"allymaxenergy":allymaxenergy,
           "enemymaxenergy": enemymaxenergy, "allyenergy": 1,
            "enemyenergy":1, "turncounter":turncounter,
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
locationList["location1"]=TemporaryLocation(1,status,locationList)
locationList["location2"]= TemporaryLocation(2,status,locationList)
locationList["location3"]= TemporaryLocation(3,status,locationList)
def resolveTie(locationList):
    allypower = locationList["location1"].alliesPower + locationList["location2"].alliesPower + locationList["location3"].alliesPower
    enemypower = locationList["location1"].enemiesPower + locationList["location2"].enemiesPower + locationList["location3"].enemiesPower
    if allypower > enemypower:
        return "Ally"
    elif allypower < enemypower:
        return "Enemy"
    else:
        return "Tie"

def checkWinner():
    locationList["location1"].locationWinner(), locationList["location2"].locationWinner(), locationList["location3"].locationWinner()
    results = [locationList["location1"].winning,locationList["location2"].winning,locationList["location3"].winning]
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
        return resolveTie(locationList)


def addUnit(unit,ally, locNum):
    selectedLoc = "location" + str(locNum)
    if(ally):
        was_added = locationList[selectedLoc].addToAllies(unit)
        if was_added:
            unit.playCard(locationList[selectedLoc])
        return was_added
    else:
        was_added = locationList[selectedLoc].addToEnemies(unit)
        unit.playCard(locationList[selectedLoc])
        print(was_added)
        if was_added:
            unit.playCard(locationList[selectedLoc])
        return was_added
    
def undoActions(turnAlly, hand):
    
    loc1temp =locationList["location1"].undoActions(turnAlly)
    loc2temp =locationList["location2"].undoActions(turnAlly)
    loc3temp =locationList["location3"].undoActions(turnAlly)
    print("temps:", loc1temp, loc2temp, loc3temp)
    refund = 0
    for unit in loc1temp + loc2temp + loc3temp:
        refund += unit.cur_cost
    hand += loc1temp + loc2temp + loc3temp
    return refund

def boardStatus(): #ritorna una stringa che definisce lo stato di ogni location 
    print(locationList["location1"].name,"[", locationList["location1"].description, "]: ",locationList["location1"].locationStatus(),"")
    print(locationList["location2"].name,"[", locationList["location2"].description, "]: ",locationList["location2"].locationStatus(),"")
    print(locationList["location3"].name,"[", locationList["location3"].description, "]: ", locationList["location3"].locationStatus(),"")

def draw(hand,deck,num): #pesca un numero di carte dal deck 
    i=0
    if deck == []:
        print("No more cards in the deck!")
    else:
        while i<num:
            hand.append(deck[-1])
            del deck[-1]
            i+=1

def gameStart(): #inserisci carte nel deck e pesca le carte
    status["allydeck"], status["enemydeck"] = [cards.Colossus(True, status),cards.Heimdall(True,status)],[cards.Scorpion(False, status),cards.Onslaught(False, status)]
    status["allydeck"].append(cards.Apocalypse(True,status))
    status["enemydeck"].append(cards.Infinaut(False,status))
    for i in range (1,5,1):
        curCard = cards.Swarm(True, status)
        status["allydeck"].append(curCard)
        curCard = cards.Nightcrawler(False, status)
        status["enemydeck"].append(curCard)
        curCard = cards.Blade(True, status)
        status["allydeck"].append(curCard)
        curCard = cards.Captainamerica(False, status)
        status["enemydeck"].append(curCard)
    random.shuffle(status["allydeck"])
    random.shuffle(status["enemydeck"])
    draw(status["allyhand"],status["allydeck"],3)
    draw(status["enemyhand"],status["enemydeck"],3)
    for location in locationList.values():
        location.startOfTurn()

def playerTurn(hand, deck,energy):
    draw(hand,deck,1)
    for location in locationList.values():
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
                boardStatus()
            case 5:
                turnenergy += undoActions(turnAlly, hand)
            case 6:
                print("Which card would you like to move?")
                moveSelection(turnAlly)
            case 8:
                if (turnAlly and not status["allysnapped"]) or (not turnAlly and not status["enemysnapped"]):
                    print("SNAP!")
                    snap(status, turnAlly)
                else: print("You already snapped!")

            case _:
                print("Input error")

def moveSelection(turnally):
    if turnally:
        units = locationList["location1"].allies + locationList["location2"].allies + locationList["location3"].allies
    else:
        units = locationList["location1"].enemies + locationList["location2"].enemies + locationList["location3"].enemies
    i=1
    print("Which card would you like to move?")
    for unit in units:
        print(i, "-", unit.location.name, " :", unit.name, " Power:", unit.cur_power)
        i+=1
    try:
        choice = int(input())
        choice -= 1
        cardToMove = units[choice]
    except:
        print("Input error")
    for moves in cardToMove.location.cards_to_move:
        if moves[0] == cardToMove:
            print("You already moved that card")
            return 0
    
    print("Where would you like to move the card?")
    i=1
    for location in locationList.values():
        if location != cardToMove.location:
            print(i, "-", location.name)
        i+=1
    try:
        choice = int(input())
        choice -= 1
        locationToMove = list(locationList.values())[choice]
    except:
        print("Input error")
    if locationToMove == cardToMove.location:
        print("You can't move the card to the same location")
    else:
        if cardToMove.moves_number > 0 or locationToMove.location_can_be_moved_to:
            if not locationToMove.checkIfLocationFull(cardToMove.ally):
                cardToMove.location.cards_to_move.append([cardToMove, locationToMove])
            else:
                print("Location full")
        else:
            print("You can't move that card!")
    


def snap(status,turnally):
    if (turnAlly and not status["allysnapped"]):
        status["allysnapped"] = True
        if not status["enemysnapped"]: status["tempcubes"] = 2
        else: status["cubes"], status["tempcubes"] = 4,4
    else:
        status["enemysnapped"] = True
        if not status["allysnapped"]: status["tempcubes"] = 2
        else: status["cubes"], status["tempcubes"] = 4,4

def startOfTurn(status):
    locationList["location1"].startOfTurn()
    locationList["location2"].startOfTurn()
    locationList["location3"].startOfTurn()
    status["allyenergy"] = status["allymaxenergy"] + status["tempenergyally"]
    status["enemyenergy"] = status["enemymaxenergy"] + status["tempenergyenemy"]
    status["tempenergyally"], status["tempenergyenemy"] = 0,0
    winning = checkWinner()
    for card in locationList["location1"].allies + locationList["location2"].allies + locationList["location3"].allies + locationList["location1"].enemies + locationList["location2"].enemies + locationList["location3"].enemies:
        card.startOfTurn()
    match winning:
        case "Ally" | "Tie":
            status["allypriority"] = True
            print("Allies have priority")
        case "Enemy":
            status["allypriority"] = False
            print("Enemies have priority")
    for card in status["allyhand"] + status["allydeck"] + status ["enemyhand"] + status["enemydeck"]:
        card.updateCard(locationList)
    draw(status["allyhand"],status["allydeck"],1)
    draw(status["enemyhand"],status["enemydeck"],1)
def announcer(status):
    match status["allypriority"]:
        case True:
            print("Revealing ally cards")
        case False:
            print("Revealing enemy cards")

def endOfTurn():
    status["cubes"] = status["tempcubes"]
    announcer(status)
    locationList["location1"].startOfTurnMoves(), locationList["location2"].startOfTurnMoves(), locationList["location3"].startOfTurnMoves()
    locationList["location1"].revealCards(), locationList["location2"].revealCards(), locationList["location3"].revealCards()
    status["allypriority"] = not status["allypriority"]
    announcer(status)
    locationList["location1"].revealCards(), locationList["location2"].revealCards(), locationList["location3"].revealCards()
    print("End of turn!")
    locationList["location1"].endOfTurn(), locationList["location2"].endOfTurn(), locationList["location3"].endOfTurn()
    status["turncounter"] +=1
    status["allymaxenergy"]+=1
    status["enemymaxenergy"]+=1


def endGame():
    boardStatus()
    winner = checkWinner()
    match winner:
        case "Ally":
            print("Allies have won ", status["cubes"]*2)
            print("Enemies have lost ", status["cubes"]*2)
        case "Enemy":
            print("Allies have lost ", status["cubes"]*2)
            print("Enemies have won ", status["cubes"]*2)
        case "Tie":
            print("Tie!") 
gameStart()
def gaming():
    while status["turncounter"]<=status["maxturns"]:
        print("Turn ", status["turncounter"],", player turn")
        print("")
        startOfTurn(status)
        boardStatus()
        turnAlly = not turnAlly
        print("Turn ", status["turncounter"],", enemy turn")
        turnAlly = not turnAlly
        status["enemyenergy"]= playerTurn(status["enemyhand"], status["enemydeck"], status["enemyenergy"])
        endOfTurn()
    endGame()
    
def turnEnd():
    endOfTurn()
    status['allypass'] = status['enemypass'] = False
    startOfTurn(status)
    status['endofturncounterally'] = status['endofturncounterenemy'] = 0

app = Flask(__name__)
def normalize_name(name):
    return name.replace(" ", "").capitalize()
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/game/ally')
def gameAlly():
    return render_template('allygame.html', status=status, locations=locationList.values())

@app.route('/game/ally/playcard', methods=['POST'])
def chooseLocationAlly():
    inputUnit = int(request.form['index'])
    return render_template('playCardAllies.html', status=status, locations=locationList.values(), card = status["allyhand"][inputUnit], cardnum = inputUnit)

@app.route('/game/ally/playcard/<locationnum>', methods=['POST'])
def playCardAlly(locationnum):
    locationToAdd = int(locationnum)+1
    inputUnit = int(request.form["card"])
    was_added = False
    if not status['allypass']:
        try:
            if status["allyenergy"] <status["allyhand"][inputUnit].cur_cost:
                print("not enough energy")
            else:
                was_added = addUnit(status["allyhand"][inputUnit], True, locationToAdd)
            if was_added:
                status["allyenergy"]-=status["allyhand"][inputUnit].cur_cost
                del status["allyhand"][inputUnit]
        except Exception as e:
            print("error")
            print(e)
    return redirect(url_for('gameAlly'))

@app.route('/game/enemy')
def gameEnemy():
    return render_template('enemygame.html', status=status, locations=locationList.values())

@app.route('/game/enemy/playcard', methods=['POST'])
def chooseLocationEnemy():
    inputUnit = int(request.form['index'])
    return render_template('playCardEnemies.html',status=status, locations=locationList.values(), card = status["enemyhand"][inputUnit], cardnum = inputUnit)

@app.route('/game/enemy/playcard/<locationnum>', methods=['POST'])
def playCardEnemy(locationnum):
    locationToAdd = int(locationnum)+1
    inputUnit = int(request.form["card"])
    was_added = False
    if not status['enemypass']:
        try:
            if status["enemyenergy"] <status["enemyhand"][inputUnit].cur_cost:
                print("not enough energy")
            else:
                was_added = addUnit(status["enemyhand"][inputUnit], False, locationToAdd)
            if was_added:
                status["enemyenergy"]-=status["enemyhand"][inputUnit].cur_cost
                del status["enemyhand"][inputUnit]
        except Exception as e:
            print("error")
            print(e)
    return redirect(url_for('gameEnemy'))

@app.route('/game/ally/pass', methods=['POST'])
def passTurnAlly():
    status["allypass"] = True
    return redirect(url_for('gameAlly'))

@app.route('/game/enemy/pass', methods=['POST'])
def passTurnEnemy():
    status["enemypass"] = True
    return redirect(url_for('gameEnemy'))

@app.route('/check_turn/<allyorenemy>')
def check_turn(allyorenemy):
    print(allyorenemy)
    passStatus = {
        'turnpassally': status['allypass'],  
        'turnpassenemy': status['enemypass'],
        'winner': "None"  
    }
    if status["allypass"] and status["enemypass"]:
        if allyorenemy == "ally":
            status["endofturncounterally"] = 1
        elif allyorenemy == "enemy":
            status["endofturncounterenemy"] = 1
        print(status["endofturncounterally"], status["endofturncounterenemy"])
        if status["endofturncounterally"] == 1 and status["endofturncounterenemy"] == 1:
            print("end turn!")    
            turnEnd()
            if status["turncounter"] > status["maxturns"]:
                endGame()
                passStatus['winner'] = checkWinner()
    return jsonify(passStatus)
    
if __name__ == "__main__":
    app.run(debug=True)

