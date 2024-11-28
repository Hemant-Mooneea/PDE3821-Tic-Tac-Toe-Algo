from algo import Algo
import requests

def getEmptyGrid():
    return [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""]
    ]

def printGrid(grid):
    for row in grid:
        print(row)

def getShapes():
    url = ""
    while True:
        try:
            response = requests.get(url)
            if requests.status_code == 200:
                data = response.json()
                return data['bot_shape'], data['player_shape'], data['current_turn']
        except:
            print(f"failed to get shape: {response.status_code}")
        time.sleep(5)

def getPlayerMove(grid):
    pass

def gameLogic(algo, grid):
    if algo.getCurrentTurn() == "PLAYER":
        playerMove = getPlayerMove(grid)
    
        if(algo.checkwin(grid)):
            return "Player wins!"
        algo.setCurrentTurn("BOT")
    
    elif algo.getCurrentTurn() == "BOT":
        botMove = algo.getBotMove(grid)
        
        if(algo.checkwin(grid)):
            return "Bot wins!"
        algo.setCurrentTurn("PLAYER")
    
    if(algo.checkDraw(grid)):
        return "Draw!"
    
    return ""

def startGame():
    botShape, playerShape, currentTurn = getShapes()
    algo = Algo(botShape, playerShape, currentTurn)
    grid = getEmptyGrid()
    gameEnded = ""
    while(gameEnded == ""):
        gameEnded = gameLogic(algo, grid)

    