from algo import Algo
from camera import Camera
from arm import Arm
from requestHandler import requestHandler

request = requestHandler()
robotArm = Arm()
# update grid array and return it
def getGrid():
    camera = Camera()

    # set arm in "watch" position to get a clear view of grid
    robotArm.moveToWatchPosition()

    #capture grid and convert to grid array
    grid = camera.main()
    
    # after "watching" the grid, move to rest position
    robotArm.moveToRestPosition()

    return grid

# general logic for the game 
def gameLogic(algo, previousGrid):
    
    if algo.getCurrentTurn() == "PLAYER":
        #wait for player to make move
        while(True):
            lastPlayed = request.getLastPlayed()
            if (lastPlayed != "" and lastPlayed == algo.getPlayerShape()):
                break
        algo.setCurrentTurn("BOT")
    
    elif algo.getCurrentTurn() == "BOT":
        robotArm.moveToRestPosition()
        # bot decides its move
        botMove = algo.getBotMove(previousGrid)
        #bot makes its move
        robotArm.moveToGrid((botMove))
        algo.setCurrentTurn("PLAYER")

    # update the grid array after move has been made
    updatedGrid = getGrid()
    if(algo.checkwin(updatedGrid, algo.playerShape)):
        return "Player win", ""
    elif(algo.checkwin(updatedGrid, algo.botShape)):
        return "Bot win", ""
    elif (algo.checkDraw(updatedGrid)):
        return "Draw", ""

    return "", updatedGrid


def startGame():
    robotArm.moveToRestPosition()
    # get the shape chosen by player, the bot shape and current turn from user interaction with website
    botShape, playerShape, currentTurn = request.getShapes()
    #initialize the algo object
    algo = Algo(botShape, playerShape, currentTurn)
    previousGrid = [["", "", ""], ["", "", ""], ["", "", ""]]
    gameEnded = ""
    while(gameEnded == ""):
        gameEnded, previousGrid = gameLogic(algo, previousGrid)
        
    if(gameEnded == "Draw"):
        robotArm.drawEmote()
    elif(gameEnded == "Player win"):
        robotArm.loseEmote()
    elif(gameEnded == "Bot win"):
        robotArm.winEmote()
        
    robotArm.moveToRestPosition()
    request.resetShapes()

def main():
    while(True):
        startGame()
main()
    

    