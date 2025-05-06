from flask import *
from gameManager import GameState

game = GameState()
game.gameStart()

app = Flask(__name__)
def normalize_name(name):
    return name.replace(" ", "").capitalize()
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/game/ally')
def gameAlly():
    print(game.status["allyhand"])
    return render_template('allygame.html', status=game.status, locations=game.locationList.values())
@app.route('/check_game_end', methods=['GET'])
def checkGameEnded():
    winner = game.passStatus['winner']
    print(game.passStatus)
    print('winner is ',winner)
    return jsonify(winner)

@app.route('/game/ally/playcard', methods=['POST'])
def chooseLocationAlly():
    inputUnit = int(request.form['index'])
    return render_template('playCardAllies.html', status=game.status, locations=game.locationList.values(), card = game.status["allyhand"][inputUnit], cardnum = inputUnit)

@app.route('/game/ally/playcard/<locationnum>', methods=['POST'])
def playCardAlly(locationnum):
    locationToAdd = int(locationnum)+1
    inputUnit = int(request.form["card"])
    was_added = False
    if not game.status['allypass']:
        try:
            if game.status["allyenergy"] < game.status["allyhand"][inputUnit].cur_cost:
                print("not enough energy")
            else:
                was_added = game.addUnit(game.status["allyhand"][inputUnit], True, locationToAdd)
            if was_added:
                game.status["allyenergy"]-=game.status["allyhand"][inputUnit].cur_cost
                del game.status["allyhand"][inputUnit]
        except Exception as e:
            print("error")
            print(e)
    return redirect(url_for('gameAlly'))

@app.route('/game/enemy')
def gameEnemy():
    return render_template('enemygame.html', status=game.status, locations=game.locationList.values())

@app.route('/game/enemy/playcard', methods=['POST'])
def chooseLocationEnemy():
    inputUnit = int(request.form['index'])
    return render_template('playCardEnemies.html',status=game.status, locations=game.locationList.values(), card = game.status["enemyhand"][inputUnit], cardnum = inputUnit)

@app.route('/game/enemy/playcard/<locationnum>', methods=['POST'])
def playCardEnemy(locationnum):
    locationToAdd = int(locationnum)+1
    inputUnit = int(request.form["card"])
    was_added = False
    if not game.status['enemypass']:
        try:
            if game.status["enemyenergy"] < game.status["enemyhand"][inputUnit].cur_cost:
                print("not enough energy")
            else:
                was_added = game.addUnit(game.status["enemyhand"][inputUnit], False, locationToAdd)
            if was_added:
                game.status["enemyenergy"]-= game.status["enemyhand"][inputUnit].cur_cost
                del game.status["enemyhand"][inputUnit]
        except Exception as e:
            print("error")
            print(e)
    return redirect(url_for('gameEnemy'))
@app.route('/game/<allyorenemy>/moveUnit', methods=['POST'])
def moveUnit(allyorenemy):
    cardnum = int(request.form["card"])
    fromlocation = int(request.form["location_num"]) + 1
    location = "location" + str(fromlocation)
    if allyorenemy == "ally":
        card = game.locationlist[location].allies[cardnum]
        return render_template('moveCardAllies.html', card = card)
    elif allyorenemy == "enemy":
        card = game.locationlist[location].enemies[cardnum]
        return render_template('moveCardEnemies.html', card = card)
@app.route('/game/<allyorenemy>/pass', methods=['POST'])
def passTurn(allyorenemy):
    if allyorenemy == "ally":
        game.status["allypass"] = True
    elif allyorenemy == "enemy":
        game.status["enemypass"] = True
    print("pass")
    
    return jsonify(success=True)

@app.route('/game/ally/movecard', methods=['POST'])
def moveCardAlly():
    return redirect(url_for('gameAlly'))

@app.route('/check_turn/<allyorenemy>')
def check_turn(allyorenemy):
    print(allyorenemy)
    if game.status["allypass"] and game.status["enemypass"]:
        if allyorenemy == "ally":
            game.status["endofturncounterally"] = 1
            game.passStatus['turnpassally'] = True

        elif allyorenemy == "enemy":
            game.status["endofturncounterenemy"] = 1
            game.passStatus['turnpassenemy'] = True

        if game.status["endofturncounterally"] == 1 and game.status["endofturncounterenemy"] == 1:
            print("End turn triggered.")
            game.turnEnd()
            print(game.passStatus)
            if game.passStatus['retreatally'] and game.passStatus['retreatenemy']:
                game.passStatus['winner'] = "Tie"
            elif game.passStatus['retreatally']:
                game.passStatus['winner'] = "Enemy"
                game.status['cubes'] /= 2
            elif game.passStatus['retreatenemy']:
                game.passStatus['winner'] = "Ally"
                game.status['cubes'] /= 2
            elif game.status["turncounter"] > game.status["maxturns"]:
                print("444444444444444444")
                game.endGame()
                game.passStatus['winner'] = game.checkWinner()
            print(game.passStatus)
    return game.passStatus

@app.route('/game/<allyorenemy>/endgame', methods=['GET'])
def endGame(allyorenemy):
    if allyorenemy == "ally":
        return render_template('endgameally.html', status=game.status, locations=game.locationList.values(), passStatus=game.passStatus)
    elif allyorenemy == "enemy":
        return render_template('endgameenemy.html', status=game.status, locations=game.locationList.values(), passStatus=game.passStatus)
@app.route("/game/startofturn", methods=['GET'])
def startOfTurn():
    print( "start of turn")	
    game.startOfTurn()
    game.status['allypass'] = False
    game.status['enemypass'] = False
    game.status['endofturncounterally'] = 0
    game.status['endofturncounterenemy'] = 0
    game.passStatus = {
            'turnpassally': game.status['allypass'],  
            'turnpassenemy': game.status['enemypass'],
            'winner': game.passStatus['winner'],
            'retreatally': game.passStatus['retreatally'],
            'retreatenemy': game.passStatus['retreatenemy'],
            'turnend': False  
        }
    return "ok"

@app.route("/game/reset", methods=['GET'])
def resetGame():
    print("reset")
    game.reset()
    return redirect((url_for('home')))

@app.route("/game/<allyorenemy>/undoActions", methods=['POST'])
def undoActions(allyorenemy):
    if allyorenemy == "ally":
        game.status["allyenergy"] += game.undoActions(True, game.status["allyhand"])
    elif allyorenemy == "enemy":
        game.status["enemyenergy"] += game.undoActions(False, game.status["enemyhand"])

    if allyorenemy == "ally": return redirect(url_for('gameAlly'))
    elif allyorenemy == "enemy": return redirect(url_for('gameEnemy')) 

@app.route("/game/<allyorenemy>/snap", methods=['POST'])
def snap(allyorenemy):
    if allyorenemy == "ally":
        game.snap(True)
        return redirect(url_for('gameAlly'))
    elif allyorenemy == "enemy":
        game.snap(False)
        return redirect(url_for('gameEnemy'))

@app.route("/game/<allyorenemy>/retreat", methods=['POST'])
def retreat(allyorenemy):
    if allyorenemy == "ally":
        game.passStatus['retreatally'] = True
        game.passStatus['turnpassally'] = True
        return redirect(url_for('gameAlly'))
    elif allyorenemy == "enemy":
        game.passStatus['retreatenemy'] = True
        game.passStatus['turnpassenemy'] = True
        return redirect(url_for('gameEnemy'))
@app.route("/game/<allyorenemy>/movecard", methods=['POST'])
def chooseLocationForMoveCard(allyorenemy):
    locationNum = int(request.form["locationNum"])
    location = game.locationList["location" + str(locationNum)]
    cardNum = int(request.form["card"])
    if allyorenemy == "ally":
        card = location.allies[cardNum]
        return render_template('moveCardsAllies.html', status=game.status, locations=game.locationList.values(), passStatus=game.passStatus, card = card)
    elif allyorenemy == "enemy":
        card = location.enemies[cardNum]
        return render_template('moveCardsEnemies.html', status=game.status, locations=game.locationList.values(), passStatus=game.passStatus, card = card)

@app.route("/game/<allyorenemy>/movecard/<locationnum>", methods=['POST'])
def confirmMove(allyorenemy, locationnum):
    result = game.moveSelection(allyorenemy, locationnum)
    if allyorenemy == "ally":
        return redirect(url_for('gameAlly'))
    elif allyorenemy == "enemy":
        return redirect(url_for('gameEnemy'))
if __name__ == "__main__":
    app.run(debug=True)



