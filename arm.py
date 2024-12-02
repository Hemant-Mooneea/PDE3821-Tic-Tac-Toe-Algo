from Arm_Lib import Arm_Device
import time
class Arm:
    def __init__(self):
        self.arm = Arm_Device()
        
        self.delay = 2500
        self.moveDelay = 1500
        self.grid_to_angles = {
            (0,0): [94, 106, 0, 24, 89, 180, self.moveDelay],
            (0,1): [87, 106, 0, 24, 89, 180, self.moveDelay],
            (0,2): [82, 106, 0, 24, 89, 180, self.moveDelay],
            (1,0): [95, 113, 0, 14, 89, 180, self.moveDelay],
            (1,1): [87, 113, 0, 14, 89, 180, self.moveDelay],
            (1,2): [81, 113, 0, 14, 89, 180, self.moveDelay],
            (2,0): [96, 120, 0, 5, 89, 180, self.moveDelay],
            (2,1): [87,120, 0, 6, 89, 180, self.moveDelay],
            (2,2): [80, 120, 0, 6, 89, 180, self.moveDelay]
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

testarm = Arm()

testarm.moveToGrid((0,2))
time.sleep(1.5)
testarm.moveToRestPosition()
time.sleep(1.5)
testarm.insertPen()
time.sleep(5.5)
testarm.moveToRestPosition()
