import random
# Global variable to keep track of the current turn
# TODO : camera.py which returns a position(eg. [0, 1],[1, 2] etc) which the player players a move
# TODO : YOLOV8 or alternatives for object detection
# TODO : game logic for the bot which will try to win, block player, random move(adjacent to another shape) in that order
# TODO : varying the difficulty of the bot by adding probability of moves

currentTurn = ""

def checkWin(grid):
    # checking rows
    for i in range(3):
        if ((grid[i][0] == grid[i][1] == grid[i][2]) and grid[i][0] != ""):
            return True
    # checking columns
    for i in range(3):
        if ((grid[0][i] == grid[1][i] == grid[2][i]) and grid[0][i] != ""):
            return True
    # checking diagonals
    if ((grid[0][0] == grid[1][1] == grid[2][2]) and grid[0][0] != ""):
        return True
    
    if ((grid[0][2] == grid[1][1] == grid[2][0]) and grid[0][2] != ""):
        return True
    # return False if no win
    return False



#SECTION: Calculating different moves and the best moves
normalMoves = [] #all moves that can be played
goodMoves = [] #moves that are likely going to secure a win or block opponent's win

def findBestMove(grid):
    
    #find the best possible moves
    for i in range(3):
        for j in range(3):
            #check for an empty grid to play
            if grid[i][j] == 0:

                #simulate playing X and see if it is a winning move
                grid[i][j] = 1
                if checkWin(grid,1):
                    goodMoves.append([i,j])
                   
                #simulate playing O and see if it is a winning move for the opponent
                grid[i][j] = 2
                if checkWin(grid,2):
                    goodMoves.append([i,j])

                #reset grid cell after simulation
                grid[i][j] = 0

    #if no good move at the moment, play wherever empty
    for i in range(3):
        for j in range(3):
            if grid[i][j] == 0:
                normalMoves.append([i,j])
                
def getPlayerMove(grid):
    # import machine learning file la apres fer li geter kotsa player la in zuer
    # e.g machine learning pou return position dan grid kt player la pu met so move
    print("hello world")
    currentTurn = "BOT"
    
def getBotMove(grid, shape):
    print("hello world")
    currentTurn = "PLAYER"
    
def gameLogic(grid, shape):
    if (currentTurn == "PLAYER"):
        getPlayerMove(grid)
        checkWin(grid)
    else:
        getBotMove(grid, shape)
        checkWin(grid)
        

def getEmptyGrid():
    # Return a 3x3 grid with all empty strings
    return [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""]
    ]
  
def printGrid(grid):
    # Print the grid in a readable format
    for row in grid:
        print(row)
        
def getShape():
    # If random is 0, then return 'X', else return 'O'
    if(random.randint(0,1) == 0):
        return 'X'
        currentTurn = "PLAYER"
        
    currentTurn = "BOT"
    return 'O'
    
def main():
    BOT_SHAPE = getShape()
    grid = getEmptyGrid()
    
    while(True):
        gameLogic(grid, BOT_SHAPE)
    
main()
    