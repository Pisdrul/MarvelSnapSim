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
            "cardsplayed": [], "onnextcardbeingplayed": []}
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


def addUnit(unit):
    loc_num = 0
    while(loc_num not in [1,2,3]):
        loc_num = int(input("Choose location: "))
    selectedLoc = "location"+str(loc_num)
    if(turnAlly):
        was_added = locationList[selectedLoc].addToAllies(unit)
        if was_added:
            unit.playCard(locationList[selectedLoc])
        return was_added
    else:
        was_added = locationList[selectedLoc].addToEnemies(unit)
        unit.playCard(locationList[selectedLoc])
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
                try:
                    inputUnit = int(input()) -1
                    if turnenergy<hand[inputUnit].cur_cost:
                        print("Not enough energy")
                    else:
                        was_added = addUnit(hand[inputUnit])
                        if was_added:
                            turnenergy-=hand[inputUnit].cur_cost
                            del hand[inputUnit]
                except:
                    print("Input error")
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
        status["allyenergy"] = playerTurn(status["allyhand"], status["allydeck"], status["allyenergy"])
        print("Turn ", status["turncounter"],", enemy turn")
        turnAlly = not turnAlly
        status["enemyenergy"]= playerTurn(status["enemyhand"], status["enemydeck"], status["enemyenergy"])
        endOfTurn()
        status["turncounter"] +=1
        status["allymaxenergy"]+=1
        status["enemymaxenergy"]+=1
    endGame()
    

app = Flask(__name__)
def normalize_name(name):
    return name.replace(" ", "").capitalize()
@app.route('/card/<card_name>')
def show_card(card_name):
    try:
        normalized_name = normalize_name(card_name)
        module = importlib.import_module(f'cards.{normalized_name}')
        CardClass = getattr(module, normalized_name)
        card = CardClass(ally=True, status={})
        return render_template('home.html', card=card)
    except (ModuleNotFoundError, AttributeError):
        abort(404)

    # Crea un'istanza della carta
    card = CardClass(ally=True, status={})
    return render_template('home.html', card=card)
@app.route('/game/ally')
def gameAlly():
    locations = locationList.values()
    return render_template('mano.html', hand=status['allyhand'])

@app.route('/game/ally/playcard', methods=['POST'])
def playCardAlly():
    index = int(request.form['index'])
    print(status['allyhand'][index].name)
    return redirect(url_for('gameAlly'))

@app.route('/game/enemy')
def gameEnemy():
    return render_template('mano.html', hand=status['enemyhand'])

@app.route('/game/enemy/playcard', methods=['POST'])
def playCardEnemy():
    index = int(request.form['index'])
    print(status['enemyhand'][index].name)
    return redirect(url_for('gameEnemy'))

if __name__ == "__main__":
    app.run(debug=True)
    
