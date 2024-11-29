from algo import Algo
import requests
import time

def getShapes():
    url = "http://127.0.0.1:5000/shape"
    while True:
        try:
            response = requests.get(url)
            data = response.json()
            if response.status_code == 200 and data['player_shape'] != "":
                return data['bot_shape'], data['player_shape'], data['current_turn']
        except Exception as e:
            print(f"failed to get shape: {e}")
        time.sleep(5)

def getPlayerMove(grid):
    # call camera.py to get the player move
    pass

def getGrid():
    # call camera.py to get the grid
    pass
    
def gameLogic(algo):
    
    if algo.getCurrentTurn() == "PLAYER":
        playerMove = getPlayerMove()
        
        if(algo.checkwin(grid)):
            return "Player wins!"
        algo.setCurrentTurn("BOT")
    
    elif algo.getCurrentTurn() == "BOT":
        grid = getGrid()
        botMove = algo.getBotMove(grid)
        
        if(algo.checkwin(grid)):
            return "Bot wins!"
        algo.setCurrentTurn("PLAYER")
    
    if(algo.checkDraw(grid)):
        return "Draw!"
    
    return ""

def resetShapes():
    url = "http://127.0.0.1:5000/shape"
    while True:
        try:
            response = requests.delete(url)
        except Exception as e:
            print(f"failed to delete shape: {e}")

def startGame():
    botShape, playerShape, currentTurn = getShapes()
    algo = Algo(botShape, playerShape, currentTurn)
    gameEnded = ""
    while(gameEnded == ""):
        gameEnded = gameLogic(algo)

    

    