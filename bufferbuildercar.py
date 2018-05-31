from car import Car
import math
import numpy as np
import random
import shared as g

class BufferBuilder(Car):

    def __init__(self, sim, lane, speed, maxspeed, id, carAhead, carUpAhead, carDownAhead, laneidx, size, canvasheight,
                 lanes):
        super(BufferBuilder, self).__init__(sim, lane, speed, maxspeed, id, carAhead, carUpAhead, carDownAhead, laneidx, size,
                                         canvasheight, lanes)
        self.aheadbufmin = 2
        self.aheadbufmax = 8
        self.accel = 0
        self.delay = 1500
        self.reaction = 0
        self.SLOWDOWN = False


    def general_behavior(self):
        # use different acceleration functins depending on difference between v0 and vF
        # currenlty just linearly accelerates(or deaccelerates) to v of front car

        if (self.ahead != None):
            if (self.aheadbufmax * self.length >= self.ahead.posx - self.posx):  # if at max buffer

                # find distance between the two cars

                dist = self.ahead.posx - self.posx - (self.aheadbufmin * self.length)


                if (self.reaction == 0): #if not reacting
                    prevAccel = self.accel #save previous accel

                    # find accel so that after dist, this car will be matching the speed of front car
                    self.accel = (math.pow(self.ahead.speedx, 2) - math.pow(self.speedx, 2)) / (dist * 2)


                    #check accel changed from + to - or vice versa
                    if ((prevAccel < 0 and self.accel > 0) or (prevAccel > 0 and self.accel < 0)):
                        self.accel = 0  #dont move car
                        #self.reaction = 100  #set delay



                else:
                    pass #self.reaction -= 1


                # update speed to reflect accel change
                self.speedx = self.speedx + self.accel
            else:
                if (self.speedx < self.maxspeed):
                    self.accel = self.speedx * .005
                    self.speedx = self.speedx + self.accel


        else:  # front car

            # for delay amount of time make car come to a stop
            if (self.SLOWDOWN and self.delay > g.TICKS):
                self.accel = self.speedx * .003
                self.speedx = self.speedx - self.accel

            # after delay accel to maxspeed
            else:
                if (self.speedx < self.maxspeed):

                    self.accel = self.speedx * .003
                    self.speedx = self.speedx + self.accel

