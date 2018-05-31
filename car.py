import shared as g
import math
import numpy as np
import random


class Car:
    def __init__(self, sim, lane, speed, maxspeed, id, carAhead, carUpAhead, carDownAhead, laneidx, size, canvasheight,
                 lanes):
        self.sim = sim
        self.length = size
        self.width = size / 2
        self.posx = -self.length
        self.posy = size / 2 + (canvasheight / 2) + self.width * 2 * (lane - (lanes / 2.0 + 1))
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
        self.color = g.carcolor
        self.name = "car"

        self.maxspeed = maxspeed
        self.inst_max = np.random.normal(self.maxspeed, self.maxspeed * .1, 1)[0]
        self.maxspeed = self.inst_max

        self.debugColorer = False
        self.debugColoring = False
        self.debugLastFirstColoring = False
        self.debugattribs = ["id", "posx", "posy", "speedx", "maxspeed", "speedy", "lane", "laneidx", "newlane",
                             "inst_max", "aheadbufmin", "aheadbufmax"]

        buffRand = np.random.normal(2, 1, size=2)
        buffRand[1] += 1
        if (buffRand[0] <= 0.7 or buffRand[0] > 1.2):
            buffRand[0] = 0.7
        if (buffRand[1] <= 3.5 or buffRand[1] > 6.0):
            buffRand[1] = 3.5

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

        if (not self.ahead == None):
            self.ahead.behind = self
        if (not self.upahead == None):
            self.upahead.downbehind = self
        if (not self.downahead == None):
            self.downahead.upbehind = self

    def setup_visual(self, c):
        self.canvas = c
        self.shape = self.canvas.create_rectangle(self.posx,
                                                  self.posy - self.width / 2,
                                                  self.posx + self.length,
                                                  self.posy + self.width / 2,
                                                  fill=self.color)

    def car_update(self):
        self.update_curlane_refs()

        # remove car?
        if (self.posx > g.ROAD_LENGTH):
            self.active = False
            if (self.behind != None):
                self.behind.ahead = None
            g.cars[self.lane - 1].remove(self)
            for c in g.cars[self.lane - 1]:
                c.laneidx = g.cars[self.lane - 1].index(c)
            if (g.GRAPHICS):
                self.canvas.delete(self.shape)
            self.sim.car_delete(self)
            return

        # change lane behavior (if ALREADY changing lane)
        if (self.changinglane):
            self.change_lane_beh()
        else:
            if (random.random() < 0.001 and self.speedx > g.SPEED_RMPH / 5.0):
                if (self.name == "autonomous"):
                    if (self.ahead == None or self.ahead.name != "autonomous"):
                        if (self.behind == None or self.behind.name != "autonomous"):
                            newlane = (self.lane - 1, self.lane + 1)[random.random() > 0.5]
                            self.attempt_lane_change(newlane)
                else:
                    newlane = (self.lane - 1, self.lane + 1)[random.random() > 0.5]
                    self.attempt_lane_change(newlane)

        # TWEAKABLE BEHAVIOR START HERE (this is where behavior-type code goes)

        self.general_behavior()

        # TWEAKABLE BEHAVIOR END HERE

        # update pos
        self.posx += self.speedx
        self.posy += self.speedy
        self.count += 1

        # update analytics
        myspeed = int(math.floor(self.speedx / self.inst_max * 5.0))
        myspeed = min(4, myspeed)
        #if(myspeed > 4.0):
        #    print("myspeed: " + str(myspeed))
        #self.sim.rSPEED_RANGE_TICKS[myspeed] += 1

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

        speedxsave = self.speedx
        speedConst = 0.921
        beta = -1.67
        gamma = -0.88
        theta = 0.78

        if (self.ahead != None):
            if ((self.aheadbufmin + 1) * self.length > (
                    self.ahead.posx - self.posx) or self.speedx > self.inst_max and self.speed > 0):
                speedConst = 15.24
                beta = 1.09
                gamma = 1.66
                theta = 0.632

                safespeedx = self.speedx + 0.0000001
                deltaSpeed = ((speedConst * pow(safespeedx, beta) / pow((self.ahead.posx - self.posx), gamma) *
                               (self.ahead.speedx - self.speedx))) / 10
                # + np.random.lognormal(0, theta, size = 1)[0])/10

                if (deltaSpeed > 0):
                    deltaSpeed = -deltaSpeed

                if (math.isnan(deltaSpeed)):
                    deltaSpeed = 0

                self.speedx += deltaSpeed

                if (self.speedx < 0):
                    self.speedx = 0.001

                if (self.ahead.posx - self.posx - self.length < self.speedx * 10 and self.speedx > self.ahead.speedx):
                    self.speedx = self.ahead.speedx


            elif ((self.aheadbufmin + 1) * self.length < (self.ahead.posx - self.posx) and self.speedx < self.inst_max):
                safespeedx = self.speedx + 0.0000001
                deltaSpeed = ((speedConst * pow(safespeedx, beta) / pow((self.ahead.posx - self.posx), gamma) *
                               (self.ahead.speedx - self.speedx))) / 10
                # + np.random.lognormal(0, theta, size = 1)[0])/10

                if (deltaSpeed < 0):
                    deltaSpeed = +deltaSpeed

                if (math.isnan(deltaSpeed)):
                    deltaSpeed = 0

                self.speedx += deltaSpeed
                self.speedx = min(self.speedx, self.maxspeed * 1.1)


        elif (self.speedx <= self.inst_max):
            self.speedx += (speedConst * (self.inst_max - self.speedx)) / 10
            self.speedx = min(self.speedx, self.inst_max)

        if (self.speedx <= 0):
            self.speedx = 0.01
        self.normal_car_impl(speedxsave)

    def laneChangeProb(self):
        randResponse = np.random.normal(1.15, 0.55, 1)[0]
        return 1 / (1 + np.exp(1.9 - 0.52 * randResponse)) * 2.12

    def attempt_lane_change(self, lane):
        self.update_upper_refs()
        self.update_lower_refs()
        if (lane > self.lane):
            if (lane <= g.LANE_COUNT):
                # if there is nothing downahead, or outside of the changelaneaheadbuf
                if (self.downahead == None or self.downahead.posx - self.posx > (
                        (self.changelaneaheadbuf + 1) * self.length)):
                    # same as above, but for downbehind
                    if (self.downbehind == None or self.posx - self.downbehind.posx > (
                            self.changelanebehindbuf + 1) * self.length):
                        self.start_change_lane(lane)
        else:
            if (lane > 0):
                # if there is nothing upahead, or outside of the changelaneaheadbuf
                if (self.upahead == None or self.upahead.posx - self.posx > (
                        (self.changelaneaheadbuf + 1) * self.length)):
                    # same as above, but for upbehind
                    if (self.upbehind == None or self.posx - self.upbehind.posx > (
                            self.changelanebehindbuf + 1) * self.length):
                        self.start_change_lane(lane)

    def normal_car_impl(self, s):
        """
        NORMAL CAR IMPLEMENTATION
        """
        self.speedx = s
        if (self.ahead != None):
            dist = self.ahead.posx - self.posx - self.length
            if (dist <= self.aheadbufmin * self.length):
                # Within min buff
                # exp_decel = self.inst_max - self.speedx / 70.0
                if (dist <= self.length * 0.1 + self.speedx):
                    self.speedx = 0
                else:
                    self.speedx -= 0.02
                # pass
            elif (dist <= self.aheadbufmax * self.length):
                # Within max buff
                # exp_accel = self.inst_max - self.speedx / 1000.0
                # self.speedx += exp_accel
                if (self.speedx < self.inst_max / 2.0):
                    self.speedx += 0.003
                else:
                    self.speedx += 0.001
                pass
            else:
                # hard accel or maintain top speed
                exp_accel = self.inst_max - self.speedx / 3000.0
                if (self.speedx < self.inst_max / 2.0):
                    self.speedx += 0.007
                else:
                    self.speedx += 0.002
                pass
        else:
            # No car ahead - hard accel or maintain top speed
            exp_accel = self.inst_max - self.speedx / 1000.0
            self.speedx += exp_accel
            pass

        # ensure speed is not past max
        self.speedx = min(self.inst_max, self.speedx)
        # ensure speed is not negative
        if (self.speedx < 0):
            self.speedx = 0

    """
    END BEHAVIOR FUNCTIONS
    """

    """
    Do not call on a non-adjacent lane
    """

    def start_change_lane(self, lane):
        if (not self.changinglane):
            self.changinglane = True
            self.newlane = lane
            self.speedy = (lane - self.lane) * self.changelanespeed
            self.laneidx = self.find_between_idx(self.posx, 0, len(g.cars[self.newlane - 1]) - 1,
                                                 g.cars[self.newlane - 1])
            g.cars[self.lane - 1].remove(self)
            g.cars[self.newlane - 1].insert(self.laneidx, self)
            for c in g.cars[self.newlane - 1]:
                c.laneidx = g.cars[self.newlane - 1].index(c)
            for c in g.cars[self.lane - 1]:
                c.laneidx = g.cars[self.lane - 1].index(c)
            self.lane = self.newlane
            self.newlane = None

    def change_lane_beh(self):
        if (False and self.newlane and abs(self.posy - (self.width + (g.HEIGHT / 2) + self.width * 2 * (
                self.newlane - (g.LANE_COUNT / 2.0 + 1)))) <= self.length):
            # if within 50% of the new lane posy, make the data transfer to the new lane (CHANGED TO 100%)
            # self.laneidx = self.find_between_idx(self.posx, 0, len(g.cars[self.newlane-1])-1, g.cars[self.newlane-1])
            # g.cars[self.lane-1].remove(self)
            # g.cars[self.newlane-1].insert(self.laneidx, self)
            # for c in g.cars[self.newlane-1]:
            #    c.laneidx = g.cars[self.newlane-1].index(c)
            # for c in g.cars[self.lane-1]:
            #    c.laneidx = g.cars[self.lane-1].index(c)
            # self.lane = self.newlane
            # self.newlane = None
            pass
        elif (abs(self.posy - (self.width + (g.HEIGHT / 2) + self.width * 2 * (
                self.lane - (g.LANE_COUNT / 2.0 + 1)))) <= self.changelanespeed):
            self.changinglane = False
            self.speedy = 0.0
            self.posy = self.width + (g.HEIGHT / 2) + self.width * 2 * (self.lane - (g.LANE_COUNT / 2.0 + 1))
            pass

    def find_between_idx(self, val, begin, end, data):
        if (len(data) == 0):
            return -1
        idx = math.ceil((end - begin + 1) / 2) - 1 + begin
        if (end - begin < 1):
            smaller = None
            bigger = None
            if (val < data[begin].posx):
                smaller = begin
                bigger = (None, begin + 1)[begin + 1 < len(data)]
            else:
                smaller = (None, begin - 1)[begin - 1 >= 0]
                bigger = begin
            # if(smaller != None):
            #    print("smaller: " + str(data[smaller].posx))
            # print("val: " + str(val))
            # if(bigger != None):
            #    print("bigger: " + str(data[bigger].posx))
            # print("smallidx: " + str(smaller))
            # print("bigidx: " + str(bigger))
            return (len(data), bigger)[bigger != None]
        if (val < data[idx].posx):
            return self.find_between_idx(val, idx + 1, end, data)
        else:
            return self.find_between_idx(val, begin, idx - 1, data)

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
            if (upaheadIdx == -1):
                self.upahead = None
                self.upbehind = None
                return
            if (len(g.cars[self.lane - 2]) > 1 and upaheadIdx != 0):
                newupbehind = None
                if (upaheadIdx < len(g.cars[self.lane - 2])):
                    newupbehind = g.cars[self.lane - 2][upaheadIdx]
                self.upbehind = newupbehind
                self.upahead = g.cars[self.lane - 2][upaheadIdx - 1]
            elif (len(g.cars[self.lane - 2]) > 0):
                if (g.cars[self.lane - 2][0].posx >= self.posx):
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
            if (downaheadIdx == -1):
                self.downbehind = None
                self.downahead = None
                return
            if (len(g.cars[self.lane]) > 1 and downaheadIdx != 0):
                newdownbehind = None
                if (downaheadIdx < len(g.cars[self.lane])):
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
        if (self.downahead != None and self.downahead.posx < self.posx):
            # shift downahead to downbehind
            newdownbehind = self.downahead
            newdownahead = self.downahead.ahead
            # fix debug color
            if (self.downbehind):
                self.downbehind.debugColoring = False
                self.downbehind.debugLastFirstColoring = True
            if (self.ahead):
                self.ahead.debugColoring = False
                self.ahead.debugLastFirstColoring = True

            self.downahead.upbehind = self.behind
            self.downahead.upahead = self
            self.downahead = newdownahead
            self.downbehind = newdownbehind
        elif (self.downbehind != None and self.downbehind.posx >= self.posx):
            # shift downbehind to downahead
            newdownbehind = self.downbehind.behind
            newdownahead = self.downbehind
            # fix debug color
            if (self.downahead != None):
                self.downahead.debugColoring = False
                self.downahead.debugLastFirstColoring = True
            if (self.behind):
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
            if (self.ahead):
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
            if (self.behind):
                self.behind.debugColoring = False
                self.behind.debugLastFirstColoring = True

            self.upbehind.downahead = self.ahead
            self.upbehind.upbehind = self
            self.upahead = newupahead
            self.upbehind = newupbehind

    def debug(self):
        # mouse over?
        if (g.DEBUG and g.GRAPHICS):
            px = g.px
            py = g.py
            if (px >= self.posx and px <= self.posx + self.length and abs(py - float(self.posy)) < self.width / 2.0):
                self.add_debug_info()
                self.debugColoring = True
                self.debugColorer = True
                self.update_curlane_refs()
                self.update_upper_refs()
                self.update_lower_refs()
                self.canvas.itemconfig(self.shape, fill="orange")

                if (self.ahead):
                    self.canvas.itemconfig(self.ahead.shape, fill="orange")
                    self.ahead.debugColoring = True

                if (self.behind):
                    self.canvas.itemconfig(self.behind.shape, fill="orange")
                    self.behind.debugColoring = True

                if (self.upahead):
                    self.canvas.itemconfig(self.upahead.shape, fill="white")
                    self.upahead.debugColoring = True

                if (self.upbehind):
                    self.canvas.itemconfig(self.upbehind.shape, fill="yellow")
                    self.upbehind.debugColoring = True

                if (self.downahead):
                    self.canvas.itemconfig(self.downahead.shape, fill="white")
                    self.downahead.debugColoring = True

                if (self.downbehind):
                    self.canvas.itemconfig(self.downbehind.shape, fill="yellow")
                    self.downbehind.debugColoring = True

            elif (self.debugColorer):
                self.debugColoring = False
                self.debugColorer = False
                self.update_curlane_refs()
                self.update_upper_refs()
                self.update_lower_refs()
                self.canvas.itemconfig(self.shape, fill=self.color)

                if (self.ahead):
                    self.canvas.itemconfig(self.ahead.shape, fill=self.color)
                    self.ahead.debugColoring = False

                if (self.upahead):
                    self.canvas.itemconfig(self.upahead.shape, fill=self.color)
                    self.upahead.debugColoring = False

                if (self.downahead):
                    self.canvas.itemconfig(self.downahead.shape, fill=self.color)
                    self.downahead.debugColoring = False

                if (self.behind):
                    self.canvas.itemconfig(self.behind.shape, fill=self.color)
                    self.behind.debugColoring = False

                if (self.upbehind):
                    self.canvas.itemconfig(self.upbehind.shape, fill=self.color)
                    self.upbehind.debugColoring = False

                if (self.downbehind):
                    self.canvas.itemconfig(self.downbehind.shape, fill=self.color)
                    self.downbehind.debugColoring = False

            # lastCar / firstCar debug coloring
            if (False and not self.debugColoring and g.DEBUG):
                if (len(g.cars[self.lane - 1]) > 0 and g.cars[self.lane - 1][-1] == self):
                    self.debugLastFirstColoring = True
                    self.canvas.itemconfig(self.shape, fill="purple")
                elif (len(g.cars[self.lane - 1]) > 0 and g.cars[self.lane - 1][0] == self):
                    self.debugLastFirstColoring = True
                    self.canvas.itemconfig(self.shape, fill="green")
                elif (self.debugLastFirstColoring):
                    self.debugLastFirstColoring = False
                    self.canvas.itemconfig(self.shape, fill=self.color)

    def update_anim(self):
        self.canvas.coords(self.shape,
                           (self.posx, self.posy - g.CAR_SIZE / 4, self.posx + g.CAR_SIZE, self.posy + g.CAR_SIZE / 4))

    def move_active(self):
        if (self.active):
            self.car_update()

    def add_debug_info(self):
        debugtext = ""
        for a in self.debugattribs:
            debugtext = debugtext + a + " " + str(self.__getattribute__(a)) + "\t"

        g.DEBUG_TEXT.set(debugtext)
