import random


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
    return 'O'
    
def main():
    BOT_SHAPE = getShape()
    grid = getEmptyGrid()
    
main()
    