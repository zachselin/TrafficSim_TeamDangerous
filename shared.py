from tkinter import *

def init_vals():
    global tk, ROAD_LENGTH, HEIGHT, LANE_HEIGHT, LANE_COUNT, DEBUG_REFERENTIAL, TICKS_UNTIL_ANIM, WIDTH, CAR_SIZE
    global SPEED_MOD, G_COUNT, ID_COUNTER, INSERT_LENGTH, ANIMATION, TICKS, TICK_MS, PAUSE, canvas, color, firstCars
    global lastCars, cars
    tk = Tk()
    # As of now, these 4 inputs dictate the simulation. LANE_HEIGHT is the pixel height of lanes, and car sizes will adjust accordingly.
    ROAD_LENGTH = 1850
    HEIGHT = 450
    LANE_HEIGHT = 15
    LANE_COUNT = 12
    DEBUG_REFERENTIAL = True
    TICKS_UNTIL_ANIM = 3000

    WIDTH = ROAD_LENGTH
    CAR_SIZE = LANE_HEIGHT
    SPEED_MOD = CAR_SIZE / 60
    G_COUNT = 0
    ID_COUNTER = 0
    INSERT_LENGTH = CAR_SIZE / 2.0
    ANIMATION = False
    TICKS = 0
    TICK_MS = 10
    PAUSE = False
    px = None
    py = None
    DEBUG_LABEL = None
    DEBUG_TEXT = None

    canvas = None
    color = 'red'
    firstCars = None
    lastCars = None
    cars = None