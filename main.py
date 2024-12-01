from algo import Algo
from camera import Camera
from requestHandler import requestHandler

def getPlayerMove(grid):
    # call camera.py to get the player move
    pass

def getGrid():
    camera = Camera()

    grid = camera.main()

    return grid
    
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

def startGame():
    request = requestHandler()
    botShape, playerShape, currentTurn = request.getShapes()
    algo = Algo(botShape, playerShape, currentTurn)
    gameEnded = ""
    while(gameEnded == ""):
        gameEnded = gameLogic(algo)
    
    request.resetShapes()
    
startGame()

    