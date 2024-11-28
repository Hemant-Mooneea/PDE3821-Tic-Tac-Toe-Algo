
#SECTION: choosing the move and playing it

def moveArmToCell(dofbot,coordinateX, coordinateY):

    #! Mapping coordinates to robot arm servo angles
    #! Assume we've already manually calibrated angles for each cell

    # Lookup table: (row, col) -> Servo angles
    coordinate_to_servo_angles = {
        (0, 0): [30, 45, 60, 90, 0, 0],  # Angles for top-left cell
        (0, 1): [35, 50, 65, 95, 0, 0],  # Angles for top-middle cell
        (0, 2): [40, 55, 70, 100, 0, 0], # Angles for top-right cell
        # etc
    }
  
    try:
        # Get angles for the cell
        angles = coordinate_to_servo_angles[(coordinateX, coordinateY)]
        for i, angle in enumerate(angles):
            print(f"Moving servo {i + 1} to {angle}°")

            # Move each servo to the specified angle
            dofbot.set_servo_angle(i + 1, angle)  

    except KeyError:

        print("Invalid grid coordinates. Please check the lookup table.")

    except Exception as e:
        
        print(f"An error occurred while moving the arm: {e}")

