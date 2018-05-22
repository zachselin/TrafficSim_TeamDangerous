from tkinter import *
import numpy as np

tk = Tk()


# As of now, these 4 inputs dictate the simulation. LANE_HEIGHT is the pixel height of lanes, and car sizes will adjust accordingly.
ROAD_LENGTH = 1850
HEIGHT = 500
LANE_HEIGHT = 20
LANE_COUNT = 7
DEBUG_REFERENTIAL = True


WIDTH = ROAD_LENGTH
CAR_SIZE = LANE_HEIGHT
SPEED_MOD = CAR_SIZE/60
G_COUNT = 0
ID_COUNTER = 0
INSERT_LENGTH = CAR_SIZE/2.0
_ANIMATION = False
TICKS = 0
PAUSE = False

canvas = None
color = 'red'
firstCars = None
lastCars = None
cars = None


class Car:
    def __init__(self, lane, speed, id, carAhead, carUpAhead, carDownAhead):
        self.length = CAR_SIZE
        self.width = CAR_SIZE/2
        self.posx = -self.length
        self.posy = CAR_SIZE/2 + (HEIGHT/2) + LANE_HEIGHT*(lane-(LANE_COUNT/2.0+1))
        self.speedx = speed
        self.speedy = 0
        self.lane = lane
        self.count = 0
        self.speed = True
        self.active = True
        self.changinglane = False
        self.id = id
        self.shape = None


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

    def setup_visual(self):
        self.shape = canvas.create_rectangle(self.posx,
                                             self.posy - self.width/2,
                                             self.posx + self.length,
                                             self.posy + self.width/2,
                                             fill=color)

    def car_update(self):
        global firstCars, cars
        # remove car?
        if(self.posx > ROAD_LENGTH):
            self.active = False
            firstCars[self.lane-1] = self.behind
            if(not self.behind == None):
                self.behind.ahead = None
            if(not self.upbehind == None):
                self.upbehind.downahead = None
            if(not self.downbehind == None):
                self.upahead = None
            cars.remove(self)

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
            if(self.ahead):
                self.ahead.debugColoring = False

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
            if(self.behind):
                self.behind.debugColoring = False

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
            if(self.ahead):
                self.ahead.debugColoring = False

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
            if(self.behind):
                self.behind.debugColoring = False

            self.upbehind.downahead = self.ahead
            self.upbehind.upbehind = self
            self.upahead = newupahead
            self.upbehind = newupbehind

    def debug(self):
        # mouse over?
        if(DEBUG_REFERENTIAL):
            px = tk.winfo_pointerx() - tk.winfo_rootx()
            py = tk.winfo_pointery() - tk.winfo_rooty()
            if(_ANIMATION):
                if(px >= self.posx and px <= self.posx + self.length and abs(py - float(self.posy)) < self.width/2.0):
                        self.debugColoring = True
                        self.debugColorer = True
                        canvas.itemconfig(self.shape, fill="orange")
                        if(self.ahead):
                            canvas.itemconfig(self.ahead.shape, fill="blue")
                            self.ahead.debugColoring = True
                        if(self.upahead):
                            canvas.itemconfig(self.upahead.shape, fill="blue")
                            self.upahead.debugColoring = True
                        if(self.downahead):
                            canvas.itemconfig(self.downahead.shape, fill="blue")
                            self.downahead.debugColoring = True
                        if(self.behind):
                            canvas.itemconfig(self.behind.shape, fill="yellow")
                            self.behind.debugColoring = True
                        if(self.upbehind):
                            canvas.itemconfig(self.upbehind.shape, fill="yellow")
                            self.upbehind.debugColoring = True
                        if(self.downbehind):
                            canvas.itemconfig(self.downbehind.shape, fill="yellow")
                            self.downbehind.debugColoring = True
                elif(self.debugColorer):
                    self.debugColoring = False
                    self.debugColorer = False
                    canvas.itemconfig(self.shape, fill="red")
                    if (self.ahead):
                        canvas.itemconfig(self.ahead.shape, fill="red")
                        self.ahead.debugColoring = False
                    if (self.upahead):
                        canvas.itemconfig(self.upahead.shape, fill="red")
                        self.upahead.debugColoring = False
                    if (self.downahead):
                        canvas.itemconfig(self.downahead.shape, fill="red")
                        self.downahead.debugColoring = False
                    if (self.behind):
                        canvas.itemconfig(self.behind.shape, fill="red")
                        self.behind.debugColoring = False
                    if (self.upbehind):
                        canvas.itemconfig(self.upbehind.shape, fill="red")
                        self.upbehind.debugColoring = False
                    if (self.downbehind):
                        canvas.itemconfig(self.downbehind.shape, fill="red")
                        self.downbehind.debugColoring = False

                # lastCar / firstCar debug coloring
                if(not self.debugColoring and DEBUG_REFERENTIAL):
                    if(lastCars[self.lane-1] == self):
                        self.debugLastFirstColoring = True
                        canvas.itemconfig(self.shape, fill="purple")
                    elif(firstCars[self.lane-1] == self):
                        self.debugLastFirstColoring = True
                        canvas.itemconfig(self.shape, fill="green")
                    elif(self.debugLastFirstColoring):
                        self.debugLastFirstColoring = False
                        canvas.itemconfig(self.shape, fill="red")


    def update_anim(self):
        #print("posx: " + str(self.posx))
        #print("count: " + str(self.count))
        #print("shape: " + str(self.shape))
        canvas.coords(self.shape, (self.posx, self.posy - CAR_SIZE/4, self.posx + CAR_SIZE, self.posy + CAR_SIZE/4))

    def move_active(self):
        if(self.active):
            self.car_update()


def init_data_structs():
    global firstCars, lastCars, cars
    firstCars = []
    lastCars = []
    cars = []
    for i in range(LANE_COUNT):
        firstCars.append(None)
        lastCars.append(None)

def init_lanes():
    global canvas
    canvas = Canvas(tk, width=WIDTH, height=HEIGHT, bg="green")
    canvas.create_line(0, (HEIGHT / 2), WIDTH, (HEIGHT / 2), width=str(LANE_HEIGHT * LANE_COUNT), fill="grey")
    canvas.pack()
    for lane in range(LANE_COUNT+1):
        line_thickness = (1, 3)[lane == 0 or lane == LANE_COUNT]
        canvas.create_line(0, (HEIGHT/2) + LANE_HEIGHT*(lane-(LANE_COUNT/2.0)), WIDTH, (HEIGHT/2) + LANE_HEIGHT*(lane-(LANE_COUNT/2.0)),
                           width=str(line_thickness), fill="white")

def make_car():
    global ID_COUNTER
    lane = np.random.randint(1, LANE_COUNT+1)
    if(lastCars[lane-1] == None or lastCars[lane-1].posx > INSERT_LENGTH):
        speed = np.random.uniform(.5*SPEED_MOD, 1*SPEED_MOD)
        # reference to ahead cars
        carUpAhead = None
        carDownAhead = None
        if(lane > 1):
            carUpAhead = lastCars[lane-2]
        if(lane < LANE_COUNT):
            carDownAhead = lastCars[lane]
        car = Car(lane, speed, ID_COUNTER, lastCars[lane-1], carUpAhead, carDownAhead)
        if(_ANIMATION):
            car.setup_visual()
        lastCars[lane-1] = car
        if(firstCars[lane-1] == None):
            firstCars[lane-1] = car
        ID_COUNTER += 1
        cars.append(car)

def init_anim():
    global cars, _ANIMATION
    init_lanes()
    for car in cars:
        car.setup_visual()
    _ANIMATION = True

def tick():
    global cars, TICKS
    TICKS += 1
    if(TICKS % 20 == 0):
        make_car()
    for car1 in cars:
        car1.ensure_references()
    for car in cars:
        car.move_active()
    if(_ANIMATION):
        for car in cars:
            car.update_anim()
            #pass
    if(DEBUG_REFERENTIAL):
        for car in cars:
            car.debug()

def control():
    global PAUSE
    if(not PAUSE):
        tick()
        tk.after(10, control)




init_data_structs()
init_anim()
control()


tk.mainloop()