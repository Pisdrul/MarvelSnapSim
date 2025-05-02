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
    print(game.passStatus)
    if game.status["allypass"] and game.status["enemypass"]:
        if allyorenemy == "ally":
            game.status["endofturncounterally"] = 1
        elif allyorenemy == "enemy":
            game.status["endofturncounterenemy"] = 1

        print(game.status["endofturncounterally"], game.status["endofturncounterenemy"])

        if game.status["endofturncounterally"] == 1 and game.status["endofturncounterenemy"] == 1:
            print("end turn!")    
            game.turnEnd()

            if game.status["turncounter"] > game.status["maxturns"]:
                game.endGame()
                game.passStatus['winner'] = game.checkWinner()
            else:
                game.startOfTurn()
            game.status['endofturncounterally'] = 0
            game.status['endofturncounterenemy'] = 0
            game.status['allypass'] = False
            game.status['enemypass'] = False

    return jsonify(game.passStatus)

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
    
if __name__ == "__main__":
    app.run(debug=True)



