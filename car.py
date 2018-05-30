import shared as g
import math
import numpy as np
import random

class Car:
    def __init__(self, lane, speed, maxspeed, id, carAhead, carUpAhead, carDownAhead, laneidx, size, canvasheight, lanes):
        self.length = size
        self.width = size/2
        self.posx = -self.length
        self.posy = size/2 + (canvasheight/2) + self.width*2*(lane-(lanes/2.0+1))
        self.speedx = speed
        self.speedy = 0
        self.lane = lane
        self.count = 0
        self.speed = True
        self.active = True
        self.changinglane = False
        self.changelanespeed = 0.01 * self.length
        self.changelaneaheadbuf = 3
        self.changelanebehindbuf = 1.5
        self.newlane = None
        self.id = id
        self.shape = None
        self.laneidx = laneidx
        self.canvas = None
        self.color = g.color

        self.maxspeed = maxspeed


        self.debugColorer = False
        self.debugColoring = False
        self.debugLastFirstColoring = False
        self.debugattribs = ["id", "posx", "posy", "speedx", "maxspeed", "speedy", "lane", "laneidx", "newlane"]

        buffRand = np.random.normal(2, 1, size = 2)
        if (buffRand[0] <= 0):
            buffRand[0] = 0.5
        if(buffRand[1] <= 0):
            buffRand[1] = 1

        # behavior control vars
        self.aheadbufmin = buffRand[0]
        self.aheadbufmax = buffRand[0] + buffRand[1]

        # `ahead` is the car that has the same lane and a posx greater-than or equal. Behind
        self.ahead = carAhead
        self.behind = None
        self.upahead = carUpAhead
        self.upbehind = None
        self.downahead = carDownAhead
        self.downbehind = None

        if(not self.ahead == None):
            self.ahead.behind = self
        if(not self.upahead == None):
            self.upahead.downbehind = self
        if(not self.downahead == None):
            self.downahead.upbehind = self

    def setup_visual(self, c):
        self.canvas = c
        self.shape = self.canvas.create_rectangle(self.posx,
                                             self.posy - self.width/2,
                                             self.posx + self.length,
                                             self.posy + self.width/2,
                                             fill=self.color)

    def car_update(self):
        self.update_curlane_refs()

        # remove car?
        if(self.posx > g.ROAD_LENGTH):
            self.active = False
            self.behind.ahead = None
            g.cars[self.lane-1].remove(self)
            for c in g.cars[self.lane-1]:
                c.laneidx = g.cars[self.lane-1].index(c)
            if(g.GRAPHICS): 
                self.canvas.delete(self.shape)
            del(self)
            return

        # change lane behavior (if ALREADY changing lane)
        if(self.changinglane):
            self.change_lane_beh()

        # TWEAKABLE BEHAVIOR START HERE (this is where behavior-type code goes)

        self.general_behavior()

        # TWEAKABLE BEHAVIOR END HERE

        # update pos
        self.posx += self.speedx
        self.posy += self.speedy
        self.count += 1

    """
    PUT BEHAVIOR FUNCTIONS HERE AS NEEDED!!!
    (Team, please put behavior-related functions here)
    """

    def general_behavior(self):
        # SPEED AND BUFFER BEHAVIOR HERE!!!!!!!! (feel free to completely gut what is here)
        # self.ahead and self.behind reference the cars that are currently ahead and behind you. Therefore,
        # to access the posx of them, do something like self.ahead.posx
        # When you define a new behavior with some sort of parameters, please go up and make it a new attribute
        # in init. That way we can easily tweak the behavior in one place
        # (the reason there are hard-coded values here is because the behavior does not currently resemble
        #  anything like that of our final behavior, at least code-wise)
        inst_max = np.random.normal(self.maxspeed, self.maxspeed * .1, 1)[0]
        speedConst = 9.21
        beta = -1.67
        gamma = -0.88
        theta = 0.78
        
        if (self.ahead != None):
            if ((self.aheadbufmin) * self.length > (self.ahead.posx - self.posx) or self.speedx > inst_max and self.speed > 0):
                speedConst = 15.24
                beta = 1.09
                gamma = 1.66
                theta = 0.632
                
                
                deltaSpeed = ((speedConst * pow(self.speedx, beta)/ pow((self.ahead.posx - self.posx),gamma) *
                (self.ahead.speedx -self.speedx)) + np.random.lognormal(0, theta, size = 1)[0])/10
                
                if(deltaSpeed > 0):
                    deltaSpeed =-deltaSpeed
                    
                if(math.isnan(deltaSpeed)):
                    deltaSpeed = 0

                self.speedx += deltaSpeed
                
                if(self.speedx < 0):
                    self.speedx = 0.01
             
                 
            elif ((self.aheadbufmin) * self.length < (self.ahead.posx - self.posx) and self.speedx < inst_max): 
                                   
                deltaSpeed = ((speedConst * pow(self.speedx, beta)/ pow((self.ahead.posx - self.posx),gamma) *
                (self.ahead.speedx -self.speedx)) + np.random.lognormal(0, theta, size = 1)[0])/10
                
                if(deltaSpeed < 0):
                    deltaSpeed =+deltaSpeed
                    
                if(math.isnan(deltaSpeed)):
                    deltaSpeed = 0

                self.speedx += deltaSpeed
                self.speedx = min(self.speedx, self.maxspeed * 1.1)
            
                
        elif(self.speedx <= inst_max):
             self.speedx += (speedConst * (inst_max -self.speedx)+ np.random.lognormal(0, theta, size = 1)[0])/10
             self.speedx = min(self.speedx, inst_max)
            
        if(self.speedx <= 0):
            self.speedx = 0.01
            
     
            
    def laneChangeProb(self):
        randResponse = np.random.normal(1.15, 0.55, 1)[0]
        return  1/(1+np.exp(1.9 - 0.52 * randResponse)[0])*2.12
    
    def attempt_lane_change(self, lane):
        self.update_upper_refs()
        self.update_lower_refs()
        if (lane > self.lane):
            if (lane <= g.LANE_COUNT):
                # if there is nothing downahead, or outside of the changelaneaheadbuf
                if (self.downahead == None or self.downahead.posx - self.posx > (
                    np.exp(2.72- 0.055 * self.speedx + np.random.normal(0, pow(1.61, 2), 1)[0])[0])):
                    # same as above, but for downbehind
                    if (self.downbehind == None or self.posx - self.downbehind.posx > (
                            self.changelanebehindbuf + 1) * self.length):
                            if(self.laneChangeProb() - 0.65 > 0.01):
                                self.start_change_lane(lane)
        else:
            if (lane > 0):
                # if there is nothing upahead, or outside of the changelaneaheadbuf
                if (self.upahead == None or self.upahead.posx - self.posx > (
                    np.exp(2.72- 0.055 * self.speedx + np.random.normal(0, pow(1.61, 2), 1)[0])[0])):
                    # same as above, but for upbehind
                    if (self.upbehind == None or self.posx - self.upbehind.posx > (
                            self.changelanebehindbuf + 1) * self.length):
                         if(self.laneChangeProb() - 0.65 > 0.01):
                                self.start_change_lane(lane)




    """
    END BEHAVIOR FUNCTIONS
    """

    """
    Do not call on a non-adjacent lane
    """
    def start_change_lane(self, lane):
        if(not self.changinglane):
            self.changinglane = True
            self.newlane = lane
            self.speedy = (lane - self.lane) * self.changelanespeed

    
    def change_lane_beh(self):
        if(self.newlane and abs(self.posy - (self.width+(g.HEIGHT/2)+self.width*2*(self.newlane-(g.LANE_COUNT/2.0+1)))) <= self.length):
            # if within 50% of the new lane posy, make the data transfer to the new lane (CHANGED TO 100%)
            self.laneidx = self.find_between_idx(self.posx, 0, len(g.cars[self.newlane-1])-1, g.cars[self.newlane-1])
            g.cars[self.lane-1].remove(self)
            g.cars[self.newlane-1].insert(self.laneidx, self)
            for c in g.cars[self.newlane-1]:
                c.laneidx = g.cars[self.newlane-1].index(c)
            for c in g.cars[self.lane-1]:
                c.laneidx = g.cars[self.lane-1].index(c)
            self.lane = self.newlane
            self.newlane = None
        elif(abs(self.posy - (self.width+(g.HEIGHT/2)+self.width*2*(self.lane-(g.LANE_COUNT/2.0+1)))) <= self.changelanespeed):
            self.changinglane = False
            self.speedy = 0.0
            self.posy = self.width+(g.HEIGHT/2)+self.width*2*(self.lane-(g.LANE_COUNT/2.0+1))
            pass

    def find_between_idx(self, val, begin, end, data):
        if(len(data) == 0):
            return -1
        idx = math.ceil((end-begin+1)/2) - 1 + begin
        if(end-begin < 1):
            smaller = None
            bigger = None
            if(val < data[begin].posx):
                smaller = begin
                bigger = (None, begin + 1)[begin + 1 < len(data)]
            else:
                smaller = (None, begin - 1)[begin - 1 >= 0]
                bigger = begin
            #if(smaller != None):
            #    print("smaller: " + str(data[smaller].posx))
            #print("val: " + str(val))
            #if(bigger != None):
            #    print("bigger: " + str(data[bigger].posx))
            #print("smallidx: " + str(smaller))
            #print("bigidx: " + str(bigger))
            return (len(data), bigger)[bigger != None]
        if(val < data[idx].posx):
            return self.find_between_idx(val, idx+1, end, data)
        else:
            return self.find_between_idx(val, begin, idx-1, data)

    def update_curlane_refs(self):
        if (self.laneidx != 0):
            self.ahead = g.cars[self.lane - 1][self.laneidx - 1]
        else:
            self.ahead = None
        if (self.laneidx < len(g.cars[self.lane - 1]) - 1):
            self.behind = g.cars[self.lane - 1][self.laneidx + 1]
        else:
            self.behind = None


    def update_upper_refs(self):
        if (self.lane > 1):
            upaheadIdx = self.find_between_idx(self.posx, 0, len(g.cars[self.lane - 2]) - 1, g.cars[self.lane - 2])
            if(upaheadIdx == -1):
                self.upahead = None
                self.upbehind = None
                return
            if(len(g.cars[self.lane - 2]) > 1 and upaheadIdx != 0):
                newupbehind = None
                if(upaheadIdx < len(g.cars[self.lane-2])):
                    newupbehind = g.cars[self.lane - 2][upaheadIdx]
                self.upbehind = newupbehind
                self.upahead = g.cars[self.lane - 2][upaheadIdx - 1]
            elif(len(g.cars[self.lane - 2]) > 0):
                if(g.cars[self.lane - 2][0].posx >= self.posx):
                    self.upahead = g.cars[self.lane - 2][0]
                    self.upbehind = None
                else:
                    self.upahead = None
                    self.upbehind = g.cars[self.lane - 2][0]
            else:
                self.upbehind = None
                self.upahead = None
        else:
            self.upahead = None
            self.upbehind = None

    def update_lower_refs(self):
        if (self.lane < g.LANE_COUNT):
            downaheadIdx = self.find_between_idx(self.posx, 0, len(g.cars[self.lane]) - 1, g.cars[self.lane])
            if(downaheadIdx == -1):
                self.downbehind = None
                self.downahead = None
                return
            if (len(g.cars[self.lane]) > 1 and downaheadIdx != 0):
                newdownbehind = None
                if(downaheadIdx < len(g.cars[self.lane])):
                    newdownbehind = g.cars[self.lane][downaheadIdx]
                self.downbehind = newdownbehind
                self.downahead = g.cars[self.lane][downaheadIdx - 1]
            elif (len(g.cars[self.lane]) > 0):
                if (g.cars[self.lane][0].posx >= self.posx):
                    self.downahead = g.cars[self.lane][0]
                    self.downbehind = None
                else:
                    self.downahead = None
                    self.downbehind = g.cars[self.lane][0]
            else:
                self.downbehind = None
                self.downahead = None
        else:
            self.downahead = None
            self.downbehind = None

    def ensure_references(self):
        # update car references
        # check for below referential integrity
        if(self.downahead != None and self.downahead.posx < self.posx):
            # shift downahead to downbehind
            newdownbehind = self.downahead
            newdownahead = self.downahead.ahead
            # fix debug color
            if(self.downbehind):
                self.downbehind.debugColoring = False
                self.downbehind.debugLastFirstColoring = True
            if(self.ahead):
                self.ahead.debugColoring = False
                self.ahead.debugLastFirstColoring = True

            self.downahead.upbehind = self.behind
            self.downahead.upahead = self
            self.downahead = newdownahead
            self.downbehind = newdownbehind
        elif(self.downbehind != None and self.downbehind.posx >= self.posx):
            # shift downbehind to downahead
            newdownbehind = self.downbehind.behind
            newdownahead = self.downbehind
            # fix debug color
            if(self.downahead != None):
                self.downahead.debugColoring = False
                self.downahead.debugLastFirstColoring = True
            if(self.behind):
                self.behind.debugColoring = False
                self.behind.debugLastFirstColoring = True

            self.downbehind.upahead = self.ahead
            self.downbehind.upbehind = self
            self.downahead = newdownahead
            self.downbehind = newdownbehind
        # check for above referential integrity
        if (self.upahead != None and self.upahead.posx < self.posx):
            # shift upahead to upbehind
            newupbehind = self.upahead
            newupahead = self.upahead.ahead
            # fix debug color
            if (self.upbehind != None):
                self.upbehind.debugColoring = False
                self.upbehind.debugLastFirstColoring = True
            if(self.ahead):
                self.ahead.debugColoring = False
                self.ahead.debugLastFirstColoring = True

            self.upahead.downbehind = self.behind
            self.upahead.downahead = self
            self.upahead = newupahead
            self.upbehind = newupbehind
        elif (self.upbehind != None and self.upbehind.posx >= self.posx):
            # shift upbehind to upahead
            newupbehind = self.upbehind.behind
            newupahead = self.upbehind
            # fix debug color
            if (self.upahead != None):
                self.upahead.debugColoring = False
                self.upahead.debugLastFirstColoring = True
            if(self.behind):
                self.behind.debugColoring = False
                self.behind.debugLastFirstColoring = True

            self.upbehind.downahead = self.ahead
            self.upbehind.upbehind = self
            self.upahead = newupahead
            self.upbehind = newupbehind

    def debug(self):
        # mouse over?
        if(g.DEBUG and g.GRAPHICS):
            px = g.px
            py = g.py
            if(px >= self.posx and px <= self.posx + self.length and abs(py - float(self.posy)) < self.width/2.0):
                self.add_debug_info()
                self.debugColoring = True
                self.debugColorer = True
                self.update_curlane_refs()
                self.update_upper_refs()
                self.update_lower_refs()
                self.canvas.itemconfig(self.shape, fill="orange")
                if(self.ahead):
                    self.canvas.itemconfig(self.ahead.shape, fill="orange")
                    self.ahead.debugColoring = True
                if(self.behind):
                    self.canvas.itemconfig(self.behind.shape, fill="orange")
                    self.behind.debugColoring = True
                if (self.upahead):
                    self.canvas.itemconfig(self.upahead.shape, fill="blue")
                    self.upahead.debugColoring = True
                if (self.upbehind):
                    self.canvas.itemconfig(self.upbehind.shape, fill="yellow")
                    self.upbehind.debugColoring = True
                if (self.downahead):
                    self.canvas.itemconfig(self.downahead.shape, fill="blue")
                    self.downahead.debugColoring = True
                if (self.downbehind):
                    self.canvas.itemconfig(self.downbehind.shape, fill="yellow")
                    self.downbehind.debugColoring = True
            elif(self.debugColorer):
                self.debugColoring = False
                self.debugColorer = False
                self.update_curlane_refs()
                self.update_upper_refs()
                self.update_lower_refs()
                self.canvas.itemconfig(self.shape, fill="red")
                if (self.ahead):
                    self.canvas.itemconfig(self.ahead.shape, fill="red")
                    self.ahead.debugColoring = False
                if (self.upahead):
                    self.canvas.itemconfig(self.upahead.shape, fill="red")
                    self.upahead.debugColoring = False
                if (self.downahead):
                    self.canvas.itemconfig(self.downahead.shape, fill="red")
                    self.downahead.debugColoring = False
                if (self.behind):
                    self.canvas.itemconfig(self.behind.shape, fill="red")
                    self.behind.debugColoring = False
                if (self.upbehind):
                    self.canvas.itemconfig(self.upbehind.shape, fill="red")
                    self.upbehind.debugColoring = False
                if (self.downbehind):
                    self.canvas.itemconfig(self.downbehind.shape, fill="red")
                    self.downbehind.debugColoring = False

            # lastCar / firstCar debug coloring
            if(not self.debugColoring and g.DEBUG):
                if(len(g.cars[self.lane-1]) > 0 and g.cars[self.lane-1][-1] == self):
                    self.debugLastFirstColoring = True
                    self.canvas.itemconfig(self.shape, fill="purple")
                elif(len(g.cars[self.lane-1]) > 0 and g.cars[self.lane-1][0] == self):
                    self.debugLastFirstColoring = True
                    self.canvas.itemconfig(self.shape, fill="green")
                elif(self.debugLastFirstColoring):
                    self.debugLastFirstColoring = False
                    self.canvas.itemconfig(self.shape, fill="red")


    def update_anim(self):
        self.canvas.coords(self.shape, (self.posx, self.posy - g.CAR_SIZE/4, self.posx + g.CAR_SIZE, self.posy + g.CAR_SIZE/4))

    def move_active(self):
        if(self.active):
            self.car_update()

    def add_debug_info(self):
        debugtext = ""
        for a in self.debugattribs:
            debugtext = debugtext + a + " " + str(self.__getattribute__(a)) + "\t"

        g.DEBUG_TEXT.set(debugtext)
