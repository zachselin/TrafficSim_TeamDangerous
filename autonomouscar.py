from car import Car
import math
import numpy as np
import random
import shared as g


class Autonomous(Car):

    def __init__(self, sim, lane, speed, maxspeed, id, carAhead, carUpAhead, carDownAhead, laneidx, size, canvasheight,
                 lanes, slowdown):
        super(Autonomous, self).__init__(sim, lane, speed, maxspeed, id, carAhead, carUpAhead, carDownAhead, laneidx, size,
                                         canvasheight, lanes, slowdown)
        self.aheadbufmin = 1.1
        self.aheadnonautobufmin = 1.3
        self.aheadbufmax = 5
        self.accel = 0
        self.delay = 1500
        self.color = g.autonomouscolor
        self.SLOWDOWN = slowdown
        self.name = "autonomous"

    def general_behavior(self):
        # use different acceleration functins depending on difference between v0 and vF
        # currenlty just linearly accelerates(or deaccelerates) to v of front car

        if (self.ahead != None):
            if (self.aheadbufmax * self.length >= self.ahead.posx - self.posx): #if at max buffer
                if(self.ahead.name == "autonomous"):
                    # find distance between the two cars
                    dist = self.ahead.posx - self.posx - (self.aheadbufmin * self.length)
                    if(dist < 0):
                        dist = 0
                    #find accel so that after dist, this car will be matching the speed of front car

                    prevAccel = self.accel
                    if(self.speedx - self.ahead.speedx != 0 and dist != 0):
                        self.accel = (math.pow(self.ahead.speedx, 2) - math.pow(self.speedx, 2)) / (dist * 2)
                        if (self.aheadbufmin * self.length >= self.ahead.posx - self.posx):
                            self.accel = self.ahead.accel
                    else:
                        self.accel = 0
                        if(dist == 0):
                            self.speedx = self.ahead.speedx * 0.95
                else:
                    # find distance between the two cars
                    dist = self.ahead.posx - self.posx - (self.aheadnonautobufmin * self.length)
                    if (dist < 0):
                        dist = 0
                    # find accel so that after dist, this car will be matching the speed of front car

                    prevAccel = self.accel
                    if (self.speedx - self.ahead.speedx != 0 and dist != 0):
                        self.accel = (math.pow(self.ahead.speedx, 2) - math.pow(self.speedx, 2)) / (dist * 2)
                        if (self.aheadnonautobufmin * self.length >= self.ahead.posx - self.posx):
                            self.accel = self.ahead.accel
                    else:
                        self.accel = 0
                        if (dist == 0):
                            self.speedx = self.ahead.speedx * 0.95

            else:
                if(self.speedx < self.maxspeed):
                    self.accel = self.speedx * .007


        else: #front car
            prevAccel = self.accel
            #for delay amount of time make car come to a stop
            if (self.SLOWDOWN and self.delay > g.TICKS):

                if(self.speedx < self.maxspeed):
                    self.accel = -self.speedx * .003

                if (self.speedx <= .1):
                    self.accel = -self.speedx

            #after delay accel to maxspeed
            else:
                if (self.speedx < self.maxspeed):
                    if(self.speedx == 0):
                        self.speedx = .05
                    self.accel = self.speedx * .005


        # update speed to reflect accel change
        self.speedx = self.speedx + self.accel
        self.speedx = min(self.inst_max, self.speedx)




            
    
            
        
   