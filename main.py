from algo import Algo
from camera import Camera
from arm import Arm
from requestHandler import requestHandler

robotArm = Arm()
# update grid array and return it
def getGrid():
    camera = Camera()

    #before capturing frame of grid, set arm in "watch" position to prevent grid obstruction
    robotArm.moveToWatchPosition()

    #capture grid and convert to grid array
    grid = camera.main()

    return grid

# general logic for the game 
def gameLogic(algo):
    
    if algo.getCurrentTurn() == "PLAYER":
        updatedGrid = None
        #wait for player to make move
        while(True):
            #check if player has made a move, see if grid has been updated
            updatedGrid = getGrid()

            #if yes, break out of loop
            if (updatedGrid != "Not Updated"):
                break
        
        algo.setCurrentTurn("BOT")
        

    elif algo.getCurrentTurn() == "BOT":
        currentGrid = getGrid()
        # bot decides its best moves from the grid
        robotArm.moveToRestPosition()
        botMove = algo.getBotMove(currentGrid)
        #bot makes its move
        robotArm.moveToGrid((botMove))

        #after making move, get updated grid array
        updatedGrid = getGrid()
        algo.setCurrentTurn("PLAYER")

    if(algo.checkwin(updatedGrid, algo.playerShape)):
        return "Player wins!"
    elif(algo.checkwin(updatedGrid, algo.botShape)):
        return "Bot wins!"
    elif (algo.checkDraw(updatedGrid)):
        return "Draw!"

    return ""


def startGame():
    robotArm.moveToRestPosition()
    request = requestHandler()
    botShape, playerShape, currentTurn = request.getShapes()
    algo = Algo(botShape, playerShape, currentTurn)
    gameEnded = ""
    while(gameEnded == ""):
        gameEnded = gameLogic(algo)
        
    print(gameEnded)
    robotArm.moveToRestPosition()
    request.resetShapes()

startGame()

    

    