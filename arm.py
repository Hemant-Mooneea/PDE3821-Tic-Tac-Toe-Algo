from Arm_Lib import Arm_Device
class Arm:
    def __init__(self):
        self.arm = Arm_Device()
        
        delay = 500
        self.grid_to_angles = {
            1: [0, 0, 0, 0, 0, 0, delay],
            2: [0, 0, 0, 0, 0, 0, delay],
            3: [0, 0, 0, 0, 0, 0, delay],
            4: [0, 0, 0, 0, 0, 0, delay],
            5: [0, 0, 0, 0, 0, 0, delay],
            6: [0, 0, 0, 0, 0, 0, delay],
            7: [0, 0, 0, 0, 0, 0, delay],
            8: [0, 0, 0, 0, 0, 0, delay],
            9: [0, 0, 0, 0, 0, 0, delay]
        }
        
    def moveToGrid(self, pos):    
        angles = self.grid_to_angles[pos]
        # Use unpacking to pass the values to Arm_serial_servo_write6
        self.arm.Arm_serial_servo_write6(*angles)
