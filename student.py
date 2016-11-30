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
    LEFT_SPEED = 190
    RIGHT_SPEED = 190


    turn_track = 0.0
    TIME_PER_DEGREE = .00922
    TURN_MODIFIER = .5



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


    ###MY NEW TURN METHODS BECAUSE encR AND encL JUST DON'T CUT
    #takes number of degrees and turns accordingly\
    # TODO: find out how to use the turn_track method to keep the robot from going backwards
    # better alternative to encR
    def turnR(self, deg):
        self.turn_track += deg
        print("the exit is " + str(self.turn_track) + " degrees away")
        self.setSpeed(self.LEFT_SPEED * self.TURN_MODIFIER,
                      self.RIGHT_SPEED * self.TURN_MODIFIER)
        right_rot()
        time.sleep(deg * self.TIME_PER_DEGREE)
        self.stop()
        self.setSpeed(self.LEFT_SPEED, self.RIGHT_SPEED)

    # better alternative to encL
    def turnL(self, deg):
        #adjust tracker so we know how far away we are from the exit
        self.turn_track -= deg
        print("the exit is " + str(self.turn_track) + " degrees away")
        self.setSpeed(self.LEFT_SPEED * self.TURN_MODIFIER,
                      self.RIGHT_SPEED * self.TURN_MODIFIER)
        left_rot()
        time.sleep(deg * self.TIME_PER_DEGREE)
        self.stop()

    # determines speed for turns
    def setSpeed(self, left, right):
        set_left_speed(int(left))
        set_right_speed(int(right))
        time.sleep(.05)


    # AUTONOMOUS DRIVING

    ## Explain the prupose of the method
    #Central logic loop of my navigation
    def nav(self):
        print("Piggy nav")
        ##### WRITE YOUR FINAL PROJECT HERE

        ### Using given/created methods
        ### main app loop
        while True:
            # loop: check that its clear
            while self.isClear():
                # lets go forward a little
                self.testDrive()
            # TODO: replace choosePath with a method that's smarter
            answer = self.choosePath()
            if answer == "left":
                # Todo: replace 30 with a variable representing a smarter option
                self.backUp
                self.turnL(30)
            elif answer == "right":
                self.backUp
                self.turnR(30)

    # major navigation code
    def testDrive(self):
        servo(81)
        time.sleep(.1)
        print("here we go!!")
        fwd()
        while True:
            if us_dist(15) < self.STOP_DIST:
                print("PTI")
                break
                # Todo: insert a method that backs away before turning
            time.sleep(.05)
            print("let's go")
        self.stop()


    """"def turnR(self, deg):
        # Two new instance variables are needed
        # 1) TIME_PER_DEGREE - .00922
        # 2) TURN_MODIFIER - .5
        print ("Let's turn " + str(deg) + " degrees right")
        print("That means I turn for " + (deg*self.TIME_FOR_DEGREE) + " seconds")

        print("Let's change motor speeds!")
        set_left_speed(self.LEFT_SPEED * self.TURN_MODIFIER)
        set_right_speed(self.RIGHT_SPEED * self.TURN_MODIFIER)

        right_rot()
        time.sleep(deg*self.TIME_PER_DEGREE)
        self.stop()

        set_left_speed(self.LEFT_SPEED)
        set_right_speed(self.RIGHT_SPEED)"""




####################################################
############### STATIC FUNCTIONS

def error():
    print('Error in input')


def quit():
    raise SystemExit


####################################################
######## THE ENTIRE APP IS THIS ONE LINE....
g = GoPiggy()
