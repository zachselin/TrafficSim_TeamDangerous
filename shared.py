from tkinter import *

def init_vals(laneNum, debug, speedlim, graphics, simlength):
    global tk, ROAD_LENGTH, HEIGHT, LANE_HEIGHT, LANE_COUNT, DEBUG_REFERENTIAL, TICKS_UNTIL_ANIM, WIDTH, CAR_SIZE
    global SPEED_MOD, G_COUNT, ID_COUNTER, INSERT_LENGTH, ANIMATION, TICKS, TICK_MS, PAUSE, canvas, color, firstCars
    global lastCars, cars, SIM_LENGTH, GRAPHICS
    tk = Tk()
    # As of now, these 4 inputs dictate the simulation. LANE_HEIGHT is the pixel height of lanes, and car sizes will adjust accordingly.
    ROAD_LENGTH = tk.winfo_screenwidth()*3/4
    HEIGHT = tk.winfo_screenheight()/2
    LANE_HEIGHT = 10
    LANE_COUNT = laneNum
    DEBUG_REFERENTIAL = debug
    TICKS_UNTIL_ANIM = 0
    SIM_LENGTH = simlength
    GRAPHICS = graphics

    WIDTH = ROAD_LENGTH
    CAR_SIZE = LANE_HEIGHT
    SPEED_MOD = CAR_SIZE / speedlim
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
    
