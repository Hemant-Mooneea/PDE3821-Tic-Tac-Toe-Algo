import random
import camera
import arm
# Global variable to keep track of the current turn
# TODO : camera.py which returns a position(eg. [0, 1],[1, 2] etc) which the player players a move
# TODO : YOLOV8 or alternatives for object detection
# TODO : game logic for the bot which will try to win, block player, random move(adjacent to another shape) in that order
# TODO : varying the difficulty of the bot by adding probability of moves

#* simulates winning and blocking moves and saves those moves to their respective arrays
def checkWin(grid, player):
    for i in range(3):
        if all(rowCell == player for rowCell in grid[i]):  # Check rows/horizontally, grid[i] represents a row
            return True
        if all(row[i] == player for row in grid):  # Check columns/vertically, check all columns at index 0,1,2
            return True
    if grid[0][0] == grid[1][1] == grid[2][2] == player:  # Check diagonal from left top to right bottom
        return True
    if grid[0][2] == grid[1][1] == grid[2][0] == player:  # Check diagonal from left bottom to right top
        return True
    #return False if no win
    return False

#* Calculating different moves and the best moves
def findBestMove(grid):
    #? robotSide and playerSide can be 1 or 2 depending on which side they chose
    #? 1 for X, 2 for O
    
    #find the best possible moves
    for i in range(3):
        for j in range(3):
            #check for an empty grid to play
            if grid[i][j] == 0:

                #simulate playing X and see if it is a winning move
                grid[i][j] = robotSide
                if checkWin(grid,robotSide):
                    winningMoves.append([i,j])
                   
                #simulate playing O and see if it is a winning move for the opponent
                grid[i][j] = playerSide
                if checkWin(grid,playerSide):
                    blockingMoves.append([i,j])

                #reset grid cell after simulation
                grid[i][j] = 0

    #if no good move at the moment, play wherever empty
    for i in range(3):
        for j in range(3):
            if grid[i][j] == 0:
                normalMoves.append([i,j])

#* captures grid each time, updates gridArray and make arm play the chosen move at its coordinates        
def robotPlay():
    gridArray = camera.captureGridAndConvertToArray()
    findBestMove(gridArray)

    if (len(winningMoves) != 0):
        chosenMove = random.choice(winningMoves)
        arm.playThisMove(chosenMove[0],chosenMove[1])
        #! after a winning move is played, game is basically over
        #! so we could stop the process here right? idk how to do it
        #! you figure it out ig

    elif (len(blockingMoves) !=0):
        chosenMove = random.choice(blockingMoves)
        arm.playThisMove(chosenMove[0],chosenMove[1])
    else:
        chosenMove = random.choice(normalMoves)
        arm.playThisMove(chosenMove[0],chosenMove[1])

#SECTION: Main code
#! had to remove the main() cause i wasn't able to access my robotSide variable inside the if function 
#? PS: how about we turn this main code into a tkinter app? then each time, it's the robot's turn,
#? PS: we press a button to let it know it's its turn

winningMoves = [] #moves that wins the game
blockingMoves = [] #moves that blocks opponent's winning moves
normalMoves = [] #basic random moves if no winning or blocking moves available
currentTurn = ""
gameOn = True
robotSide = 0

#! this is just a draft
print("Welcome!\n")

#! there could probably be start button in the tkinter app
#! and these would be shown after pressing start

playerSide = int(input("What side do you want to play on? \n1.X \n2.O \nChoice: "))

if (playerSide == 1):
    robotSide = 2
    currentTurn = "player"
else:
    robotSide = 1
    currentTurn = "robot"
    robotPlay()

#! then after the robot has played, the player will play right
#! and after he finishes, he clicks on another button called "Robot's turn" or idk
#! and it re-executes robotPlay() each time it's clicked

#* press button
    robotPlay()
    

    
    