from Arm_Lib import Arm_Device
import time
class Arm:
    def __init__(self):
        self.arm = Arm_Device()
        
        self.delay = 2500
        self.moveDelay = 1500
        self.grid_to_angles = {
            (0,2): [83, 79.5, 0, 29, 90, 180,self.moveDelay],
            (0,1): [90, 80, 0, 28, 90, 180, self.moveDelay],
            (0,0): [96, 79.5, 0, 29, 90, 180, self.moveDelay],
            (1,2): [83, 83, 0, 21, 90, 180, self.moveDelay],
            (1,1): [90, 83, 0, 20, 90, 180, self.moveDelay],
            (1,0): [97, 83.5, 0, 20, 90, 180, self.moveDelay],
            (2,2): [82, 86, 0, 13, 90, 180, self.moveDelay],
            (2,1): [90, 87, 0, 12, 90, 180, self.moveDelay],
            (2,0): [98, 86, 0, 13, 90, 180, self.moveDelay]
        }
        
    def moveToGrid(self, pos):    
        angles = self.grid_to_angles[pos]
        # Use unpacking to pass the values to Arm_serial_servo_write6
        self.arm.Arm_serial_servo_write6(*angles)
        time.sleep(1.5)
        self.moveToRestPosition()
        time.sleep(3)

    def moveToWatchPosition(self):
        self.arm.Arm_serial_servo_write6(90,90,0,5,90,180,self.delay)
        
    def moveToRestPosition(self):
        self.arm.Arm_serial_servo_write6(90,180,0,0,90,180,self.delay)
    
    def insertPen(self):
        self.arm.Arm_serial_servo_write6(88,116,0,13,89,110,self.delay)
        time.sleep(10)
        self.arm.Arm_serial_servo_write6(88,116,0,13,89,180,self.delay)
        time.sleep(5)
        self.moveToRestPosition()
    def checkPen(self):
        self.arm.Arm_serial_servo_write6(88,116,0,13,89,180,self.delay)            
    def testAllGrids(self):
        for i in range(3):
            for j in range(3):
                self.moveToGrid((i,j))
                time.sleep(1.5)   
                self.testArm.moveToRestPosition()
                time.sleep(3)   