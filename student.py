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
    STOP_DIST = 20

    # CONSTRUCTOR
    def __init__(self):
        print("Piggy has be instantiated!")
        # this method makes sure Piggy is looking forward
        #self.calibrate()
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        while True:
            self.stop()
            self.handler()

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

    def status(self):
        print('my power is at ' + str(volt()) + " volts")





    # AUTONOMOUS DRIVING
    def nav(self):
        print("Piggy nav")
        ##### WRITE YOUR FINAL PROJECT HERE
        #TODO : IF while loop fails, check for other paths
        #loop: check that it's clear
        '''while self.isClear():
            #go forward a bit
            encF(15)
            #trying to complete the TODO

        if not self.isClear():
            self.encB(5)
            self.encR(9)
            self.encF(10)
            self.encL(9)'''
        while True:
            while self.isClear():
                self.encF(20)
                answer= self.choosePath()
                if answer == "left":
                    self.encL(8)
                    self.flushScan()
                elif answer == "right":
                    self.encR(8)
                    self.flushScan()


####################################################
############### STATIC FUNCTIONS

def error():
    print('Error in input')


def quit():
    raise SystemExit


####################################################
######## THE ENTIRE APP IS THIS ONE LINE....
g = GoPiggy()
