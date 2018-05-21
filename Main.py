from tkinter import *
import numpy as np

tk = Tk()


# As of now, these 4 inputs dictate the simulation. LANE_HEIGHT is the pixel height of lanes, and car sizes will adjust accordingly.
ROAD_LENGTH = 1850
HEIGHT = 500
LANE_HEIGHT = 20
LANE_COUNT = 7



WIDTH = ROAD_LENGTH
CAR_SIZE = LANE_HEIGHT
SPEED_MOD = CAR_SIZE/60

G_COUNT = 0
ID_COUNTER = 0


canvas = None
color = 'red'
firstCars = None
lastCars = None

def initDataStructs():
    global firstCars, lastCars
    firstCars = []
    lastCars = []
    for i in range(LANE_COUNT):
        firstCars.append(None)
        lastCars.append(None)

def initLanes():
    global canvas
    canvas = Canvas(tk, width=WIDTH, height=HEIGHT, bg="green")
    canvas.create_line(0, (HEIGHT / 2), WIDTH, (HEIGHT / 2), width=str(LANE_HEIGHT * LANE_COUNT), fill="grey")
    canvas.pack()
    for lane in range(LANE_COUNT+1):
        line_thickness = (1, 3)[lane == 0 or lane == LANE_COUNT]
        canvas.create_line(0, (HEIGHT/2) + LANE_HEIGHT*(lane-(LANE_COUNT/2.0)), WIDTH, (HEIGHT/2) + LANE_HEIGHT*(lane-(LANE_COUNT/2.0)),
                           width=str(line_thickness), fill="white")


class Car:
    def __init__(self, lane, speed, id, carAhead, carUpAhead, carDownAhead, anim=True):
        self.length = CAR_SIZE
        self.width = CAR_SIZE/2
        self.posx = -self.length
        self.posy = CAR_SIZE/2 + (HEIGHT/2) + LANE_HEIGHT*(lane-(LANE_COUNT/2.0+1))
        self.speedx = speed
        self.speedy = 0
        self.lane = lane
        self.count = 0
        self.anim = anim
        self.speed = True
        self.active = True
        self.changinglane = False
        self.id = id
        self.shape = None


        self.isOn = False



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

        if(anim):
            self.setupVisual()
            print(canvas.coords(self.shape))
        print(str(self.posx))
        print(str(self.posy))
        self.move_active()

    def setupVisual(self):
        self.anim = True
        self.shape = canvas.create_rectangle(self.posx,
                                             self.posy - self.width/2,
                                             self.posx + self.length,
                                             self.posy + self.width/2,
                                             fill=color)

    def decelerate(self):
        self.speedx *= .90
        if (self.speedx < 0.5):
            self.speed = False

    def accelerate(self):
        self.speedx *= 1.10
        if (self.speedx > 2.0):
            self.speed = True

    def car_update(self):
        global firstCars
        # remove car
        if(self.posx > ROAD_LENGTH):
            self.active = False
            firstCars[self.lane-1] = self.behind
            if(not self.behind == None):
                self.behind.ahead = None
            if(not self.upbehind == None):
                self.upbehind.downahead = None
            if(not self.downbehind == None):
                self.upahead = None

        # update pos
        self.posx += self.speedx
        self.posy += self.speedy

        # update car references
        # check for below referential integrity
        if(self.downahead != None and self.downahead.posx < self.posx):
            # shift downahead to downbehind
            newdownbehind = self.downahead
            newdownahead = self.downahead.ahead
            self.downahead.upbehind = self.behind
            self.downahead.upahead = self

            # fix debug color
            canvas.itemconfig(self.downahead.shape, fill="red")

            self.downahead = newdownahead
            self.downbehind = newdownbehind
        if(self.downbehind != None and self.downbehind.posx >= self.posx):
            # shift downbehind to downahead
            newdownbehind = self.downbehind.behind
            newdownahead = self.downbehind
            self.downbehind.upahead = self.ahead
            self.downbehind.upbehind = self

            # fix debug color
            canvas.itemconfig(self.downbehind.shape, fill="red")

            self.downahead = newdownahead
            self.downbehind = newdownbehind

        # update anim
        if(self.anim):
            self.update_anim()

        # basic buffer behavior
        if(self.ahead != None):
            if((self.aheadbufmin+1) * self.length > (self.ahead.posx - self.posx)):
                if((self.aheadbufmin+1) * self.length/2 > self.ahead.posx - self.posx):
                    self.speedx = self.ahead.speedx
                self.speedx *= 0.8
            elif((self.aheadbufmax+1) * self.length < (self.ahead.posx - self.posx)):
                self.speedx *= 1.05
                self.speedx = min(self.speedx, self.ahead.speedx * 1.1)

        # mouse over?
        if(self.id >= 0):
            px = tk.winfo_pointerx() - tk.winfo_rootx()
            py = tk.winfo_pointery() - tk.winfo_rooty()
            if(px >= self.posx and px <= self.posx + self.length and abs(py - float(self.posy)) < self.width/2.0):
                self.isOn = True
                canvas.itemconfig(self.shape, fill="orange")
                if(self.ahead):
                    canvas.itemconfig(self.ahead.shape, fill="blue")
                if(self.upahead):
                    canvas.itemconfig(self.upahead.shape, fill="blue")
                if(self.downahead):
                    canvas.itemconfig(self.downahead.shape, fill="blue")
                if(self.behind):
                    canvas.itemconfig(self.behind.shape, fill="yellow")
                if(self.upbehind):
                    canvas.itemconfig(self.upbehind.shape, fill="yellow")
                if(self.downbehind):
                    canvas.itemconfig(self.downbehind.shape, fill="yellow")
            elif(self.isOn):
                self.isOn = False
                canvas.itemconfig(self.shape, fill="red")
                if (self.ahead):
                    canvas.itemconfig(self.ahead.shape, fill="red")
                if (self.upahead):
                    canvas.itemconfig(self.upahead.shape, fill="red")
                if (self.downahead):
                    canvas.itemconfig(self.downahead.shape, fill="red")
                if (self.behind):
                    canvas.itemconfig(self.behind.shape, fill="red")
                if (self.upbehind):
                    canvas.itemconfig(self.upbehind.shape, fill="red")
                if (self.downbehind):
                    canvas.itemconfig(self.downbehind.shape, fill="red")

        # behavior
        if (self.count == 50):
            #if (self.speed):
            #    self.decelerate()
            #else:
            #    self.accelerate()
            self.count = 0
            if (not self.upahead == None):
                print("posx of upahead: " + str(self.upahead.posx))
                #print("ahead's posx of me: " + str(self.ahead.behind.posx))
                print("posx: " + str(self.posx))
        else:
            self.count = self.count + 1


    def update_anim(self):
        canvas.coords(self.shape, (self.posx, self.posy - CAR_SIZE/4, self.posx + CAR_SIZE, self.posy + CAR_SIZE/4))

    def move_active(self):
        if(self.active):
            self.car_update()
            tk.after(10, self.move_active) # changed from 10ms to 30ms

def make_car():
    global ID_COUNTER
    lane = np.random.randint(1, LANE_COUNT+1)
    speed = np.random.uniform(.5*SPEED_MOD, 1*SPEED_MOD)

    # reference to ahead cars
    carUpAhead = None
    carDownAhead = None
    if(lane > 1):
        carUpAhead = lastCars[lane-2]
    if(lane < LANE_COUNT):
        carDownAhead = lastCars[lane]
    car = Car(lane, speed, ID_COUNTER, lastCars[lane-1], carUpAhead, carDownAhead, True)
    lastCars[lane-1] = car
    if(firstCars[lane-1] == None):
        firstCars[lane-1] = car
    ID_COUNTER += 1
    tk.after(1000, make_car)
initDataStructs()
initLanes()
make_car()


tk.mainloop()