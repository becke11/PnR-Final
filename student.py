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
                "TT": ('test turn', self.testTurn),
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
        ### Using given/created methods
        ### main app loop
        while True:
            # loop: check that its clear
            if self.isClear():
                # lets go forward a little
                self.cruise()
            # back ups before turn
            self.backUp()
            turn_target = self.kenny()
            # which way to turn
            if turn_target < 0:
                self.turnR(abs(turn_target))
            else:
                self.turnL(turn_target)


            """if answer == "left":
                self.turnL(30)
                # self.turnL(turn_target)
            elif answer == "right":
                # back up before turn to not hit anything
                encB(7)
                self.turnR(30)
                # self.turnR(turn_target)
            else:
                print("I can't find a path")"""

    #################################
    ### THE KENNY METHOD OF SCANNING - experimental

    def kenny(self):
        #Activate our scanner!
        self.wideScan()
        # count will keep track of contiguous positive readings
        count = 0
        # list of all the open paths we detect
        option = [0]
        #YOU DECIDE: What do we add to STOP_DIST when looking for a path fwd?
        SAFETY_BUFFER = 30
        #YOU DECIDE: what increment do you have your wideScan set to?
        INC = 2

        ###########################
        ######### BUILD THE OPTIONS
        #loop from the 60 deg right of our middle to 60 deg left of our middle
        for x in range(self.MIDPOINT - 60, self.MIDPOINT + 60):
            # ignore all blank spots in the list
            if self.scan[x]:
                # add 30 if you want, this is an extra safety buffer
                if self.scan[x] > (self.STOP_DIST + SAFETY_BUFFER):
                    count += 1
                # if this reading isn't safe...
                else:
                    # aww nuts, I have to reset the count, this path won't work
                    count = 0
                #YOU DECIDE: Is 16 degrees the right size to consider as a safe window?
                if count > (16 / INC) - 1:
                    # SUCCESS! I've found enough positive readings in a row
                    print("---FOUND OPTION: from " + str(x - 16) + " to " + str(x))
                    #set the counter up again for next time
                    count = 0
                    #add this option to the list
                    option.append(x - 8)

        ####################################
        ############## PICK FROM THE OPTIONS - experimental

        #The biggest angle away from our midpoint we could possibly see is 90
        bestoption = 90
        #the turn it would take to get us aimed back toward the exit - experimental
        ideal = -self.turn_track
        print("\nTHINKING. Ideal turn: " + str(ideal) + " degrees\n")
        # x will iterate through all the angles of our path options
        for x in option:
            # skip our filler option
            if x != 0:
                # the change to the midpoint needed to aim at this path
                turn = self.MIDPOINT - x
                # state our logic so debugging is easier
                print("\nPATH @  " + str(x) + " degrees means a turn of " + str(turn))
                # if this option is closer to our ideal than our current best option...
                if abs(ideal - bestoption) > abs(ideal - turn):
                    # store this turn as the best option
                    bestoption = turn
        if bestoption > 0:
            input("\nABOUT TO TURN RIGHT BY: " + str(bestoption) + " degrees")
        else:
            input("\nABOUT TO TURN LEFT BY: " + str(abs(bestoption)) + " degrees")
        return bestoption

    def backUp(self):
        if us_dist(15) < 10:
            print("Too close. Backing up for half a second")
            bwd()
            time.sleep(.5)
            self.stop()

    #########################################
    ### SCANNER - move head to take sensor readings

    def wideScan(self):
        #dump all values that might be in our list
        self.flushScan()
        #YOU DECIDE: What increment should we use when scanning?
        for x in range(self.MIDPOINT-60, self.MIDPOINT+60, +2):
            # move the sensor that's mounted to our servo
            servo(x)
            #give some time for the servo to move
            time.sleep(.1)
            #take our first measurement
            scan1 = us_dist(15)
            time.sleep(.1)
            #double check the distance
            scan2 = us_dist(15)
            #if I found a different distance the second time....
            if abs(scan1 - scan2) > 2:
                scan3 = us_dist(15)
                time.sleep(.1)
                #take another scan and average? the three together - you decide
                scan1 = (scan1+scan2+scan3)/3
            self.scan[x] = scan1
            print("Degree: "+str(x)+", distance: "+str(scan1))
            time.sleep(.01)



    # This method drives forward as long as nothing's in the way
    def cruise(self):
        # Extra credit: Upgrade this so it looks around while driving
        # Use the GoPiGo API's method to aim the sensor forward
        servo(self.MIDPOINT)
        #give the robot time to move
        time.sleep(.05)
        # start driving forward
        fwd()
        # start an infinite loop
        while True:
            # break the loop if the sensor reading is closer than our stop dist
            if us_dist(15) < self.STOP_DIST:
                break
            #YOU DECIDE: How many seconds do you wait in between a check?
            time.sleep(.05)
        # stop if the sensor loop broke
        self.stop()

    # method to test turning
    def testTurn(self):
        print("let's see if our tracking is accurate")
        self.turnR(50)
        self.turnL(60)
        input("Am I about 10 degrees from the exit?")
        self.turnL(80)
        input(" Am I about 90 degrees from the start?")



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
