import shared as g

class Car:
    def __init__(self, lane, speed, id, carAhead, carUpAhead, carDownAhead, laneidx, size, canvasheight, lanes):
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
        self.id = id
        self.shape = None
        self.laneidx = laneidx
        self.canvas = None
        self.color = g.color


        self.debugColorer = False
        self.debugColoring = False
        self.debugLastFirstColoring = False



        # behavior control vars
        self.aheadbufmin = 1.0
        self.aheadbufmax = 2.0

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
        # remove car?
        if(self.posx > g.ROAD_LENGTH):
            self.active = False
            g.firstCars[self.lane-1] = self.behind
            if(not self.behind == None):
                self.behind.ahead = None
            if(not self.upbehind == None):
                self.upbehind.downahead = None
            if(not self.downbehind == None):
                self.upahead = None
            g.cars[self.lane-1].remove(self)
            del(self)
            return

        # basic buffer behavior
        if (self.ahead != None):
            if ((self.aheadbufmin + 1) * self.length > (self.ahead.posx - self.posx)):
                if ((self.aheadbufmin + 1) * self.length / 2 > self.ahead.posx - self.posx):
                    self.speedx = self.ahead.speedx
                self.speedx *= 0.95
            elif ((self.aheadbufmax + 1) * self.length < (self.ahead.posx - self.posx)):
                if (self.ahead.speedx / float(self.speedx) < 0.7):
                    self.speedx += 0.05
                else:
                    # gradual speedup
                    self.speedx *= 1.02
                self.speedx = min(self.speedx, self.ahead.speedx * 1.1)

        # update pos
        self.posx += self.speedx
        self.posy += self.speedy
        self.count += 1



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
        if(g.DEBUG_REFERENTIAL and g.ANIMATION):
            px = g.tk.winfo_pointerx() - g.tk.winfo_rootx()
            py = g.tk.winfo_pointery() - g.tk.winfo_rooty()
            if(px >= self.posx and px <= self.posx + self.length and abs(py - float(self.posy)) < self.width/2.0):
                    self.debugColoring = True
                    self.debugColorer = True
                    self.canvas.itemconfig(self.shape, fill="orange")
                    if(self.ahead):
                        self.canvas.itemconfig(self.ahead.shape, fill="blue")
                        self.ahead.debugColoring = True
                    if(self.upahead):
                        self.canvas.itemconfig(self.upahead.shape, fill="blue")
                        self.upahead.debugColoring = True
                    if(self.downahead):
                        self.canvas.itemconfig(self.downahead.shape, fill="blue")
                        self.downahead.debugColoring = True
                    if(self.behind):
                        self.canvas.itemconfig(self.behind.shape, fill="yellow")
                        self.behind.debugColoring = True
                    if(self.upbehind):
                        self.canvas.itemconfig(self.upbehind.shape, fill="yellow")
                        self.upbehind.debugColoring = True
                    if(self.downbehind):
                        self.canvas.itemconfig(self.downbehind.shape, fill="yellow")
                        self.downbehind.debugColoring = True
            elif(self.debugColorer):
                self.debugColoring = False
                self.debugColorer = False
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
            if(not self.debugColoring and g.DEBUG_REFERENTIAL):
                if(g.lastCars[self.lane-1] == self):
                    self.debugLastFirstColoring = True
                    self.canvas.itemconfig(self.shape, fill="purple")
                elif(g.firstCars[self.lane-1] == self):
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