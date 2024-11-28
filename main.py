from algo import Algo

def getEmptyGrid():
    return [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""]
    ]

def printGrid(grid):
    for row in grid:
        print(row)

def getBotShape():
    pass    

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
    botShape, playerShape, currentTurn = getBotShape()
    algo = Algo(botShape, playerShape, currentTurn)
    grid = getEmptyGrid()
    gameEnded = ""
    while(gameEnded == ""):
        gameEnded = gameLogic(algo, grid)

    