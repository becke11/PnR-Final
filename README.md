# PnR-Final
The final project for my Programming and Robotics class
Purpose: to find the most efficient way to get through a maze of boxes to the exit


self.stop() A more reliable stop command. It repeats the GoPiGo's stop() method three times to assure that the command is not lost.

self.wideScan() This will fill your self.scan array with distances self.MIDPOINT-60, self.MIDPOINT+60, +2

self.flushScan() Resets the list that stores the distances of the ultrasonic sensor.

self.status() Prints your current power level, motor speeds, midpoint and stop distance. If one of your ideas isn't working the way you want it to, you can add a couple status updates in your code to help you see what's happening with your robot.

self.calibrate() This method is built into the class GoPiggy's initilization. When you first start your app, it will ask you to calibrate the midpoint and the motor speeds. Note: The values that you receive in this method will not be saved unless you update the variables at the top of your code

self.isClear() Will perform a three point check around self.MIDPOINT and will return True if no distance is shorter than the stop dist.

self.turnR()/self.turnL() This will uses degrees and time.sleep in order to make a turn and tracks these turns in turn_track. Is used later with the kenny method in self.nav

self.kenny() This allows the GoPiGo to choose a path that is closest to the exit. Prevents the robot from going backwards

self.nav() The central brain for this project. Combines self.kenny and self.turnL/self.turnR in order for the GoPiGo to navigate through the maze of boxes

self.rotate() allows user to apply a speed modifier to the robot during the turn for a certain amount of time in order to see how long it would take to turn 90 degrees.

self.handler() used so the user can choose which method to use at the moment,

self.testTurn() makes sure that the time.sleep for degrees still tracks turns correctly

self.testDrive() cruise method that only stops when the robot's sensors detect something in its way

self.backUp() this backs the GoPiGo up in before turning so it doesn't hit anything

self.setSpeed() sets the speed at which the robot will go


Ideas for the Future
In the future, I would like to be able to create a method that allowed the GoPiGo to scan while it is driving.
Also. I would like to be able to use some device like a camera or a GPS in order to make turns and tracking more accurate


