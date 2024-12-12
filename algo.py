import random

class Algo:
    # Constructor to initialize the botShape, playerShape and currentTurn
    def __init__(self, botShape, playerShape, currentTurn):
        self.botShape = botShape
        self.playerShape = playerShape
        self.currentTurn = currentTurn
    # Setter method to set the current turn
    def setCurrentTurn(self, currentTurn):
        self.currentTurn = currentTurn
    # Getter method to get the current turn
    def getCurrentTurn(self):
        return self.currentTurn
    # Getter method to get the botShape
    def getBotShape(self):
        return self.botShape
    # Getter method to get the playerShape
    def getPlayerShape(self):
        return self.playerShape
    # Method which checks if a player has won the game by checking the rows, columns and diagonals
    def checkwin(self, grid, shape):
        # Checking rows
        for i in range(3):
            if grid[i][0] == grid[i][1] == grid[i][2] == shape:
                return True
        # Checking columns
        for i in range(3):
            if grid[0][i] == grid[1][i] == grid[2][i] == shape:
                return True
        # Checking diagonals
        if grid[0][0] == grid[1][1] == grid[2][2] == shape:
            return True
        if grid[0][2] == grid[1][1] == grid[2][0] == shape:
            return True
        # If no winning combination is found, return False
        return False
    # Method to find the winning moves for the bot
    def findWinningMoves(self, grid, shape):
        # List to store the winning moves
        winningMoves = []
        # Loop through the grid
        for i in range(3):
            for j in range(3):
                if grid[i][j] == "":
                    #simulating the move
                    grid[i][j] = shape
                    if self.checkwin(grid, shape):
                        winningMoves.append([i,j])
                    grid[i][j] = ""
        return winningMoves
    # Method to find the adjacent moves for the bot   
    def findAdjacentMoves(self, grid):
        # Set to store the unique moves(no duplicates)
        uniqueMoves = set()
        # Loop through the grid
        for i in range(3):
            for j in range(3):
                # Check if the current position is occupied by the bot
                if grid[i][j] == self.botShape:
                    # If the current position is occupied by the bot, check the adjacent positions
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
        return list(uniqueMoves)

    # Method to find the other moves for the bot
    def findOtherMoves(self, grid):
        otherMoves = []
        for i in range(3):
            for j in range(3):
                if grid[i][j] == "":
                    otherMoves.append([i,j])
        return otherMoves
    # Method to find the center move for the bot
    def findCenterMove(self, grid):
        if grid[1][1] == "":
            return [1,1]
        return None
    # Method to find the corner moves for the bot
    def findCornerMove(self, grid):
        # List to store the corner moves
        cornerMoves = []
        # Check if the any corner is empty
        if grid[0][0] == "":
            cornerMoves.append([0,0])
        if grid[0][2] == "":
            cornerMoves.append([0,2])
        if grid[2][0] == "":
            cornerMoves.append([2,0])
        if grid[2][2] == "":
            cornerMoves.append([2,2])
        return cornerMoves
    # Method to check if the game is a draw
    def checkDraw(self, grid):
        # Loop through the grid
        for i in range(3):
            for j in range(3):
                # If any cell is empty, return False
                if(grid[i][j] == ""):
                    return False
        return True
    # Method to get the bot move by passing the grid
    def getBotMove(self, grid):
        # Obtain the winning moves for the bot
        winningMoves = self.findWinningMoves(grid, self.botShape)
        # If there are winning moves, return a random move from the winning moves
        if winningMoves:
            return random.choice(winningMoves)
        # Obtain the blocking moves for the bot
        blockingMoves = self.findWinningMoves(grid, self.playerShape)
        # If there are blocking moves, return a random move from the blocking moves
        if blockingMoves:
            return random.choice(blockingMoves)  
        # Obtain the center move for the bot
        centerMove = self.findCenterMove(grid)
        # If there is a center move, return the center move
        if centerMove:
            return centerMove
        # Obtain the corner moves for the bot
        cornerMoves = self.findCornerMove(grid)
        # If there are corner moves, return a random move from the corner moves
        if cornerMoves:
            return random.choice(cornerMoves)
        # Obtain the adjacent moves for the bot
        adjacentMoves = self.findAdjacentMoves(grid)
        # If there are adjacent moves, return a random move from the adjacent moves
        if adjacentMoves:
            return random.choice(adjacentMoves)  
        # Obtain the other moves for the bot
        otherMoves = self.findOtherMoves(grid)
        # If there are other moves, return a random move from the other moves
        if otherMoves:
            return random.choice(otherMoves) 
        # If no move is found, return None
        return None 
