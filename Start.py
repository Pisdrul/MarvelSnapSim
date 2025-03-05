power1,power2,power3 = 0,0,0
allies_loc1,allies_loc2, allies_loc3 = [], [], []
enemies_loc1,enemies_loc2, enemies_loc3 = [], [], []
exit = False
turnAlly = False
def addTolocation(location, unit):
    if(len(location)<4):
        location.append(unit)
        return True
    else:
        print("Location full")
        return False
def checkWinner():
    alli
def addUnit(unit):
    loc_num = 0
    print("Ally turn?", turnAlly)
    while(loc_num not in [1,2,3]):
        loc_num = int(input("Choose location: "))
        print(loc_num)
    match loc_num:
        case 1:
            if(turnAlly):
                print("Adding Allies")
                return addTolocation(allies_loc1, unit)
            else:
                print("Adding Enemies")
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
    
    

while not exit:
    turnAlly = not turnAlly
    userInput = input("""Press 1 to print state;
Press 2 to add a unit;
Press 3 to exit;
Press 4 to check for winner;                      
""")
    match userInput:
        case "1":
            print("Location 1:",allies_loc1, " vs ", enemies_loc1)
            print("Location 1:",allies_loc1, " vs ", enemies_loc1)
            print("Location 1:",allies_loc1, " vs ", enemies_loc1)
        case "2":
            print("AddUnit")
            power = int(input("Input unit power: "))
            print (addUnit(power))
        case "3":
            print("Bye bye!")
            exit = True
        case "4":
            CheckWinner()
        case _:
            print("InputError")
    
    