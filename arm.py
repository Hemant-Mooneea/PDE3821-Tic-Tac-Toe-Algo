from Arm_Lib import Arm_Device
import time
class Arm:
    def __init__(self):
        self.arm = Arm_Device()
        self.delay = 1500
        self.grid_to_angles = {
            (0,2): [95, 85, 0, 10, 90, 180, self.delay],
            (0,1): [86, 85, 0, 10, 90, 180, self.delay],
            (0,0): [79, 85, 0, 10, 90, 180, self.delay],
            (1,2): [95, 82, 0, 18, 90, 180, self.delay],
            (1,1): [86, 82, 0, 18, 90, 180, self.delay],
            (1,0): [79, 82, 0, 18, 90, 180, self.delay],
            (2,2): [94.5, 78, 0, 26, 90, 180, self.delay],
            (2,1): [87.5, 78, 0, 26, 90, 180, self.delay],
            (2,0): [80.5, 78, 0, 26, 90, 180, self.delay]
        }
        
    def moveToGrid(self, pos):    
        angles = self.grid_to_angles[tuple(pos)]
        # Use unpacking to pass the values to Arm_serial_servo_write6
        self.arm.Arm_serial_servo_write6(*angles)
        time.sleep(1.5)
        self.moveToRestPosition()

    def moveToWatchPosition(self):
        self.arm.Arm_serial_servo_write6(90,95,0,0,90,180,self.delay)
        time.sleep(1.5)
        
    def moveToRestPosition(self):
        self.arm.Arm_serial_servo_write6(90,180,0,0,90,180,self.delay)
        time.sleep(1.5)
          
    def testAllGrids(self):
        for i in range(3):
            for j in range(3):
                self.moveToGrid((i,j))