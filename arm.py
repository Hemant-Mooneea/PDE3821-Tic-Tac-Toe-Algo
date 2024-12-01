from Arm_Lib import Arm_Device
class Arm:
    def __init__(self):
        self.arm = Arm_Device()
        
        delay = 500
        self.grid_to_angles = {
            (0,0): [0, 0, 0, 0, 0, 0, delay],
            (0,1): [0, 0, 0, 0, 0, 0, delay],
            (0,2): [0, 0, 0, 0, 0, 0, delay],
            (1,0): [0, 0, 0, 0, 0, 0, delay],
            (1,1): [0, 0, 0, 0, 0, 0, delay],
            (1,2): [0, 0, 0, 0, 0, 0, delay],
            (2,0): [0, 0, 0, 0, 0, 0, delay],
            (2,1): [0, 0, 0, 0, 0, 0, delay],
            (2,2): [0, 0, 0, 0, 0, 0, delay]
        }
        
    def moveToGrid(self, pos):    
        angles = self.grid_to_angles[pos]
        # Use unpacking to pass the values to Arm_serial_servo_write6
        self.arm.Arm_serial_servo_write6(*angles)

    def moveToWatchPosition(self):
        self.arm.Arm_serial_servo_write6("//enter angles for watch grid position")

