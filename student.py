import pigo
import time
import random
from gopigo import *

'''
This class INHERITS your teacher's Pigo class. That means Mr. A can continue to
improve the parent class and it won't overwrite your work.
'''


class GoPiggy(pigo.Pigo):
    # CUSTOM INSTANCE VARIABLES GO HERE. You get the empty self.scan array from Pigo
    # You may want to add a variable to store your default speed
    MIDPOINT = 81
    STOP_DIST = 30
    speed = 100
    TURNSPEED = 195

    # Used to make the engines equal
    def setSpeed(self, x):
        self.speed = x
        set_left_speed(self.speed)
        set_right_speed(self.speed * .5)

    def getSpeed(self):
        return self.speed


    # CONSTRUCTOR
    def __init__(self):
        print("Piggy has be instantiated!")
        # this method makes sure Piggy is looking forward
        #self.calibrate()
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        while True:
            self.stop()
            self.handler()
        self.setSpeed(self.LEFT_SPEED, self.RIGHT_SPEED)

    ##### HANDLE IT
    def handler(self):
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like
        menu = {"1": ("Navigate forward", self.nav),
                "2": ("Rotate", self.rotate),
                "3": ("Dance", self.dance),
                "4": ("Calibrate servo", self.calibrate),
                "s": ('status', self.status),
                "q": ("Quit", quit)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        #
        ans = input("Your selection: ")
        menu.get(ans, [None, error])[1]()

    def turnL(self, x):
        previous = self.getSpeed()
        self.setSpeed(self.TURNSPEED)
        self.encL(x)
        self.setSpeed(previous)

    # A SIMPLE DANCE ALGORITHM
    def dance(self):
        print("Is it safe to dance?")
        ##### WRITE YOUR FIRST PROJECT HERE
        for x in range(100, 200, 50):
            if not self.isClear():
                print("NOT SAFE. TURN BACK NOW")
                break
            else:
                print ('Speed is set to ' + str(x))
                self.choosePath()
                set_speed(x)
                servo(20)
                self.encR(40)
                servo(40)
                servo(45)
                servo(50)
                servo(40)
                self.choosePath()
                self.encB(6)
                self.encL(40)
                servo(60)
                self.encB(9)
                self.encR(3)
                self.encL(3)
                self.encR(3)
                self.encB(3)
                servo(80)
                self.encR(18)
                servo(100)
                self.choosePath()
                self.encB(5)
                self.encL(6)
                servo(120)
                self.encF(2)
                time.sleep(.1)
                x += 50

    def status(self):
        print('my power is at ' + str(volt()) + " volts")


    # AUTONOMOUS DRIVING
    def nav(self):
        print("Piggy nav")
        ##### WRITE YOUR FINAL PROJECT HERE
        #TODO : IF while loop fails, check for other paths
        """while True:
            while self.isClear():
                self.encF(10)
                answer = self.choosePath()
                if answer == "left":
                    self.encL(8)
                    self.flushScan()
                elif answer == "right":
                    self.encR(8)
                    self.flushScan()"""

        while True:
            # loop: check that its clear
            while self.isClear():
                # lets go forward a little
                self.testDrive()
            answer = self.choosePath()
            if answer == "left":
                self.encL(5)
            elif answer == "right":
                self.encR(5)

    ##Test Drive Method
    def testDrive(self):
        servo(81)
        time.sleep(.1)
        print("here we go!!")
        fwd()
        while True:
            if us_dist(15) < self.STOP_DIST:
                print("PTI")
                break
            time.sleep(.05)
            print("let's go")
        self.stop()

####################################################
############### STATIC FUNCTIONS

def error():
    print('Error in input')


def quit():
    raise SystemExit


####################################################
######## THE ENTIRE APP IS THIS ONE LINE....
g = GoPiggy()
