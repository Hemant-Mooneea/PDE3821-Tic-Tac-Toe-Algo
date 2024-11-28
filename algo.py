import random
# TODO : camera.py which returns a position(eg. [0, 1],[1, 2] etc) which the player players a move
# TODO : YOLOV8 or alternatives for object detection

# Global variable to keep track of the current turn
currentTurn = ""

# checks if any player has won by checking rows, columns and diagonals
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

# Function to find the winning moves for the bot
def findWinningMoves(grid, winningMoves, BOT_SHAPE): 
    for i in range(3):
        for j in range(3):
            if(grid[i][j] == ""):
                grid[i][j] = BOT_SHAPE
                if(checkWin(grid)):
                    winningMoves.append([i,j])
                grid[i][j] = ""
                
# Function to find the blocking moves for the bot
def findBlockingMoves(grid, blockingMoves, PLAYER_SHAPE):
    for i in range(3):
        for j in range(3):
            if(grid[i][j] == ""):
                grid[i][j] = PLAYER_SHAPE
                if(checkWin(grid)):
                    blockingMoves.append([i,j])
                grid[i][j] = ""
# Function to find the adjacent moves for the bot
def findAdjacentMoves(grid, adjacentMoves, BOT_SHAPE):
    uniqueMoves = set()

    for i in range(3):
        for j in range(3):
            if grid[i][j] == BOT_SHAPE:
                # Checking top, bottom, left and right of the current position for empty grid
                if (i - 1 >= 0 and grid[i - 1][j] == ""):
                    uniqueMoves.add((i - 1, j)) 
                if (i + 1 < 3 and grid[i + 1][j] == ""):
                    uniqueMoves.add((i + 1, j))
                if (j - 1 >= 0 and grid[i][j - 1] == ""):
                    uniqueMoves.add((i, j - 1))
                if (j + 1 < 3 and grid[i][j + 1] == ""):
                    uniqueMoves.add((i, j + 1))
    
    # Convert the set to a list before returning
    adjacentMoves.extend(list(uniqueMoves))

# Function to find the diagonal moves for the bot
def findDiagonalMoves(grid, diagonalMoves, BOT_SHAPE):
    if grid[1][1] == BOT_SHAPE:
        if grid[0][0] == "":
            diagonalMoves.append([0,0])
        if grid[0][2] == "":
            diagonalMoves.append([0,2])
        if grid[2][0] == "":
            diagonalMoves.append([2,0])
        if grid[2][2] == "":
            diagonalMoves.append([2,2])

# Function to find the other moves for the bot
def findOtherMoves(grid, otherMoves):
    for i in range(3):
        for j in range(3):
            if grid[i][j] == "":
                otherMoves.append([i,j])

def getBotMove(grid, BOT_SHAPE, PLAYER_SHAPE):
    winningMoves = []
    diagonalMoves = []  
    adjacentMoves = []
    blockingMoves = []
    otherMoves = []
    
    findWinningMoves(grid, winningMoves, BOT_SHAPE)
    findBlockingMoves(grid, blockingMoves, PLAYER_SHAPE)
    findDiagonalMoves(grid, diagonalMoves, BOT_SHAPE)
    findAdjacentMoves(grid, adjacentMoves, BOT_SHAPE)
    findOtherMoves(grid, otherMoves)
    
def checkDraw(grid):
    for i in range(3):
        for j in range(3):
            if(grid[i][j] == ""):
                return False
    return True

def checkGameEnd(grid, currentTurn, ):
    if(checkWin(grid) and currentTurn == "PLAYER"):
        print("Player wins!")
        return True
    elif(checkWin(grid) and currentTurn == "BOT"):
        print("Bot wins!")
        return True
    elif(checkDraw(grid)):
        print("Draw!")
        return True
    
    return False

def updateGrid(grid, move, shape):
    grid[move[0]][move[1]] = shape
    
def gameLogic(grid, BOT_SHAPE, PLAYER_SHAPE):
    global currentTurn
    
    if (currentTurn == "PLAYER"):
        playerMove = getPlayerMove(grid)
        updateGrid(grid, playerMove, PLAYER_SHAPE)
        currentTurn = "BOT"
    else:
        botMove = getBotMove(grid, BOT_SHAPE, PLAYER_SHAPE)
        updateGrid(grid, botMove, BOT_SHAPE)
        currentTurn = "PLAYER"
        
    printGrid(grid)
    
    if(checkGameEnd(grid, currentTurn)):
        return True

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
    global currentTurn
    # If random is 0, then bot is 'X', else bot is 'O'
    if(random.randint(0,1) == 0):
        currentTurn = "PLAYER"
        return 'X', 'O'
        
    currentTurn = "BOT"
    return 'O', 'X'
    
def startGame():
    global currentTurn
    BOT_SHAPE, PLAYER_SHAPE = getShape()
    grid = getEmptyGrid()
    while(True):
        if(gameLogic(grid, BOT_SHAPE, PLAYER_SHAPE)):
            break
def main():
    startGame()
    
main()
    