import random

class Algo:
    def __init__(self, botShape, playerShape, currentTurn):
        self.botShape = botShape
        self.playerShape = playerShape
        self.currentTurn = currentTurn
        
    def setCurrentTurn(self, currentTurn):
        self.currentTurn = currentTurn
        
    def getCurrentTurn(self):
        return self.currentTurn
    
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
        
        return False
    
    def findWinningMoves(self, grid, shape):
        winningMoves = []
        for i in range(3):
            for j in range(3):
                if grid[i][j] == "":
                    #simulating the move
                    grid[i][j] = shape
                    if self.checkwin(grid, shape):
                        winningMoves.append([i,j])
                    grid[i][j] = ""
        return winningMoves
                    
    def findAdjacentMoves(self, grid):
        uniqueMoves = set()
        for i in range(3):
            for j in range(3):
                if grid[i][j] == self.botShape:
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

    # Function to find the other moves for the bot
    def findOtherMoves(self, grid):
        otherMoves = []
        for i in range(3):
            for j in range(3):
                if grid[i][j] == "":
                    otherMoves.append([i,j])
        return otherMoves
    
    def findCenterMove(self, grid):
        if grid[1][1] == "":
            return [1,1]
        return None
    
    def findCornerMove(self, grid):
        cornerMoves = []
        if grid[0][0] == "":
            cornerMoves.append([0,0])
        if grid[0][2] == "":
            cornerMoves.append([0,2])
        if grid[2][0] == "":
            cornerMoves.append([2,0])
        if grid[2][2] == "":
            cornerMoves.append([2,2])
        return cornerMoves
    
    def checkDraw(self, grid):
        for i in range(3):
            for j in range(3):
                if(grid[i][j] == ""):
                    return False
        return True

    def getBotMove(self, grid):
        winningMoves = self.findWinningMoves(grid, self.botShape)
        if winningMoves:
            return random.choice(winningMoves)
        
        blockingMoves = self.findWinningMoves(grid, self.playerShape)
        if blockingMoves:
            return random.choice(blockingMoves)  

        centerMove = self.findCenterMove(grid)
        if centerMove:
            return centerMove
    
        cornerMoves = self.findCornerMove(grid)
        if cornerMoves:
            return random.choice(cornerMoves)
        
        adjacentMoves = self.findAdjacentMoves(grid)
        if adjacentMoves:
            return random.choice(adjacentMoves)  
        
        otherMoves = self.findOtherMoves(grid)
        if otherMoves:
            return random.choice(otherMoves) 
         
        return None 
