import random

#SECTION: Detecting grid cells


#? using opencv to capture frame of grid

#! add opencv code here



#* use yolo model or whatever to scan grid cells, separate them using bounding boxes and label them as coordinates 
#* such as (0,0), (0,1), etc and determine whether its empty, filled with X or O


#! add code here for detection




""" Each of those coordinates will then be assigned a value depending on what they contain
# a dictionary could be used to store these key-value pairs as such: (0,0):0 (empty), (0,1):1 (filled with X)
? 0: empty grid cell
? 1: represents X
? 2: represents O
"""

#example of said dictionary
coordinateValueDict = {
    (0, 0): 0,  
    (0, 1): 1,  
    (0, 2): 2, 
    (1, 0): 0,
    (1, 1): 2,
    (1, 2): 1,
    (2, 0): 0,
    (2, 1): 0,
    (2, 2): 1,
    #etc
}

#*default starting grid, will get updated as game proceeds
grid = [[0,0,0],
        [0,0,0],
        [0,0,0]]

#* updating the grid as per the dictionary
for (row,col), value in coordinateValueDict.items():
    grid[row][col] = value
    

#SECTION: Checking if player has won

def checkWin(grid, player):
    
    for i in range(3):
        #checking rows
        if all(row == player for row in grid[i]):
            return True
        #checking columns
        if all(column[i] == player for column in grid):
            return True

    #checking diagonal from top to bottom
    if grid[0][0] == grid[1][1] == grid[2][2] == player:
        return True
        #checking diagonal from bottom to top
    if grid[0][2] == grid[1][1] == grid[2][0] == player:
        return True
    
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


#SECTION: choosing the move and playing it

#?choose a random move from the good moves array, if no good moves available
#?then choose a random move from the normal moves array

#to be randomly generated
indexChosen = random.randint(0,2)
move_chosen = goodMoves[indexChosen]


#! Mapping coordinates to robot arm servo angles
#! Assume we've already manually calibrated angles for each cell

#maybe we could manually moves the arm to the center of each grid and record the angles used?
#idk just speculating but i think it could be done

# Lookup table: (row, col) -> Servo angles
grid_to_servo_angles = {
    (0, 0): [30, 45, 60, 90, 0, 0],  # Angles for top-left cell
    (0, 1): [35, 50, 65, 95, 0, 0],  # Angles for top-middle cell
    (0, 2): [40, 55, 70, 100, 0, 0], # Angles for top-right cell
    # etc
}

# Function to move the arm to a cell
def move_to_cell(row, col):
    angles = grid_to_servo_angles[(row, col)]  # Get angles for the cell
    for i, angle in enumerate(angles):
        # Command each servo to the angle
        print(f"Moving servo {i + 1} to {angle}°")
        # Add actual Yahboom SDK servo movement code here
        # e.g., dofbot.set_servo_angle(i + 1, angle)

# Example move: Robot chooses (1, 2)
move_to_cell(move_chosen[0], move_chosen[1])


        

