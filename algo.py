import random
# Global variable to keep track of the current turn
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
    