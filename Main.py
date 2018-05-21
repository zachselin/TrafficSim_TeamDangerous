from tkinter import *
import numpy as np

tk = Tk()


# As of now, these 4 inputs dictate the simulation. LANE_HEIGHT is the pixel height of lanes, and car sizes will adjust accordingly.
ROAD_LENGTH = 1850
HEIGHT = 500
LANE_HEIGHT = 7
LANE_COUNT = 7



WIDTH = ROAD_LENGTH
CAR_SIZE = LANE_HEIGHT
SPEED_MOD = CAR_SIZE/60

G_COUNT = 0
IDS = 0


canvas = None
color = 'red'


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
    def __init__(self, lane, speed, id, anim=True):
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
        if(self.posx > ROAD_LENGTH):
            self.active = False
        self.posx += self.speedx
        self.posy += self.speedy
        if(self.anim):
            self.update_anim()
        if (self.count == 50):
            if (self.speed):
                self.decelerate()
            else:
                self.accelerate()
            self.count = 0
        else:
            self.count = self.count + 1


    def update_anim(self):
        canvas.coords(self.shape, (self.posx, self.posy - CAR_SIZE/4, self.posx + CAR_SIZE, self.posy + CAR_SIZE/4))

    def move_active(self):
        if(self.active):
            self.car_update()
            tk.after(10, self.move_active) # changed from 10ms to 30ms

def make_car():
    global IDS
    lane = np.random.randint(1, LANE_COUNT+1)
    speed = np.random.uniform(.5*SPEED_MOD, 1*SPEED_MOD)
    car = Car(lane, speed, IDS, True)
    IDS += 1
    tk.after(200, make_car)
initLanes()
make_car()


tk.mainloop()