
#! moon if you seeing this, it's just a draft for me, relax, take a chill pill
#! need to import algo.py
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
