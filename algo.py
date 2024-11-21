import random
# Global variable to keep track of the current turn
# 1 for player, 0 for bot
currentTurn = 0

def gameLogic(grid, shape):
    print("hello world")

def getPlayerMove(grid):
    # import machine learning file la apres fer li geter kotsa player la in zuer
    # e.g machine learning pou return position dan grid kt player la pu met so move
    print("hello world")
    
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
        currentTurn = 0
        
    currentTurn = 1   
    return 'O'
    
def main():
    BOT_SHAPE = getShape()
    grid = getEmptyGrid()
    gameLogic(grid, BOT_SHAPE)
    
main()
    