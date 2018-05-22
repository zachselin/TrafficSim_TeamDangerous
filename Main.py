import shared as g
from car import Car
import numpy as np


def init_data_structs():
    g.tk.bind("<space>", pause)
    g.firstCars = []
    g.lastCars = []
    g.cars = []
    for i in range(g.LANE_COUNT):
        g.firstCars.append(None)
        g.lastCars.append(None)
        g.cars.append([])

def init_lanes():
    g.canvas = g.Canvas(g.tk, width=g.WIDTH, height=g.HEIGHT, bg="green")
    g.canvas.create_line(0, (g.HEIGHT / 2), g.WIDTH, (g.HEIGHT / 2), width=str(g.LANE_HEIGHT * g.LANE_COUNT), fill="grey")
    g.canvas.pack()
    for lane in range(g.LANE_COUNT+1):
        line_thickness = (1, 3)[lane == 0 or lane == g.LANE_COUNT]
        g.canvas.create_line(0, (g.HEIGHT/2) + g.LANE_HEIGHT*(lane-(g.LANE_COUNT/2.0)), g.WIDTH, (g.HEIGHT/2) + g.LANE_HEIGHT*(lane-(g.LANE_COUNT/2.0)),
                           width=str(line_thickness), fill="white")

def init_anim():
    init_lanes()
    for lane in g.cars:
        for car in lane:
            car.setup_visual(g.canvas)
        g.ANIMATION = True

def make_car():
    lane = np.random.randint(1, g.LANE_COUNT+1)
    if(g.lastCars[lane-1] == None or g.lastCars[lane-1].posx > g.INSERT_LENGTH):
        speed = np.random.uniform(.5*g.SPEED_MOD, 1*g.SPEED_MOD)
        # reference to ahead cars
        carUpAhead = None
        carDownAhead = None
        if(lane > 1):
            carUpAhead = g.lastCars[lane-2]
        if(lane < g.LANE_COUNT):
            carDownAhead = g.lastCars[lane]
        car = Car(lane, speed, g.ID_COUNTER, g.lastCars[lane-1], carUpAhead, carDownAhead, len(g.cars[lane-1]), g.CAR_SIZE, g.HEIGHT, g.LANE_COUNT) # last param is index in lane list
        if(g.ANIMATION):
            car.setup_visual(g.canvas)
        g.lastCars[lane-1] = car
        if(g.firstCars[lane-1] == None):
            g.firstCars[lane-1] = car
        g.ID_COUNTER += 1
        g.cars[lane-1].append(car)

def pause(event):
    g.PAUSE = (not g.PAUSE)

def tick():
    if(g.TICKS % 20 == 0):
        make_car()
    if(not g.PAUSE):
        for lane in g.cars:
            for car in lane:
                car.ensure_references()
        for lane in g.cars:
            for car in lane:
                car.move_active()
    if(g.ANIMATION and not g.PAUSE):
        for lane in g.cars:
            for car in lane:
                car.update_anim()
    if(g.DEBUG_REFERENTIAL):
        for lane in g.cars:
            for car in lane:
                car.debug()
    g.TICKS += 1

def control():
    tick()
    g.tk.after(g.TICK_MS, control)

def start():
    g.init_vals()
    init_data_structs()
    for it in range(g.TICKS_UNTIL_ANIM):
        tick()
    init_anim()
    control()
    g.tk.mainloop()

start()