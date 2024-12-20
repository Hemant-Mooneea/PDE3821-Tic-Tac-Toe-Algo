from Arm_Lib import Arm_Device
import time
class Arm:
    def __init__(self):
        self.arm = Arm_Device()
        self.delay = 1500
        # hard coding the angles for the 9 grid coordinates
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
    
    # move the arm to the grid coordinate passed as argument
    def moveToGrid(self, pos):    
        angles = self.grid_to_angles[tuple(pos)]
        # Use unpacking to pass the values to Arm_serial_servo_write6
        self.arm.Arm_serial_servo_write6(*angles)
        time.sleep(1.5)
        self.moveFromGridToWatch()
        self.moveToWatchPosition()

    # move arm to a position where the camera module can look clearly at the grid
    def moveToWatchPosition(self):
        self.arm.Arm_serial_servo_write6(90,95,0,0,90,180,self.delay)
        time.sleep(1.5)
    
    # move arm to rest after tapping the screen, preventing obstruction of grid while playing
    def moveToRestPosition(self):
        self.arm.Arm_serial_servo_write6(90,180,0,0,90,180,self.delay)
        time.sleep(0.75)
    
    # temporary position before moving to watch position to prevent pen sliding
    def moveFromGridToWatch(self):
        self.arm.Arm_serial_servo_write6(90,150,0,0,90,180,750)
        time.sleep(0.75)

    # tests whether arm can accurately tap each grid cell
    def testAllGrids(self):
        for i in range(3):
            for j in range(3):
                self.moveToRestPosition()
                angles = self.grid_to_angles[tuple((i,j))]
                # Use unpacking to pass the values to Arm_serial_servo_write6
                self.arm.Arm_serial_servo_write6(*angles)
                time.sleep(1.5)
        self.moveToRestPosition()
    
    # perform a set of motions upon losing
    def loseEmote(self):
        self.moveToRestPosition()
        self.arm.Arm_serial_servo_write6(90,100,0,0,90,180,self.delay)
        time.sleep(1.5)
        for i in range(3):
            self.arm.Arm_serial_servo_write6(50,100,0,0,90,180,1000)
            time.sleep(1)
            self.arm.Arm_serial_servo_write6(130,100,0,0,90,180,1000)
            time.sleep(1)
        self.moveToRestPosition()

    # perform a set of motions upon making a draw
    def drawEmote(self):
        self.moveToRestPosition()
        for i in range(3):
            self.arm.Arm_serial_servo_write6(90,180,0,-10,90,180,500)
            time.sleep(0.5)
            self.arm.Arm_serial_servo_write6(90,180,0, 10,90,180,500)
            time.sleep(0.5)
        self.moveToRestPosition()

    # perform a set of motions upon winning
    def winEmote(self):
        self.moveToRestPosition()
        for i in range(3):
            self.arm.Arm_serial_servo_write6(45,180,0,10,90,180,750)
            time.sleep(0.75)
            self.arm.Arm_serial_servo_write6(135,180,0,10,90,180,750)
            time.sleep(0.75)
            self.arm.Arm_serial_servo_write6(45,180,0,0,90,180,750)
            time.sleep(0.75)
            self.arm.Arm_serial_servo_write6(135,180,0,0,90,180,750)
            time.sleep(0.75)
        self.moveToRestPosition()
