from Arm_Lib import Arm_Device
class Arm:
    def __init__(self):
        self.arm = Arm_Device()
        
        self.delay = 500
        self.grid_to_angles = {
            (0,0): [0, 0, 0, 0, 0, 0, self.delay],
            (0,1): [0, 0, 0, 0, 0, 0, self.delay],
            (0,2): [0, 0, 0, 0, 0, 0, self.delay],
            (1,0): [0, 0, 0, 0, 0, 0, self.delay],
            (1,1): [0, 0, 0, 0, 0, 0, self.delay],
            (1,2): [0, 0, 0, 0, 0, 0, self.delay],
            (2,0): [96, 115, 0, 14, 89, 180, self.delay],
            (2,1): [87,114, 0, 14, 89, 180, self.delay],
            (2,2): [80, 114, 0, 15, 89, 180, self.delay]
        }
        
    def moveToGrid(self, pos):    
        angles = self.grid_to_angles[pos]
        # Use unpacking to pass the values to Arm_serial_servo_write6
        self.arm.Arm_serial_servo_write6(*angles)

    def moveToWatchPosition(self):
        self.arm.Arm_serial_servo_write6(90,90,0,5,180,180,self.delay)
        
    def moveToRestPosition(self):
        self.arm.Arm_serial_servo_write6(90,180,0,0,90,180,self.delay)
    
    def insertPen(self):
        self.arm.Arm_serial_servo_write6(88,116,0,13,89,180,self.delay)
