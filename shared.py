from tkinter import *

def init_vals(root, laneNum, debug, speedlim, graphics, simlength, tickstilanim, carsPerMin):
    global tk, ROAD_LENGTH, HEIGHT, LANE_HEIGHT, LANE_COUNT, DEBUG, TICKS_UNTIL_ANIM, WIDTH, CAR_SIZE
    global SPEED_RMPH, G_COUNT, ID_COUNTER, INSERT_LENGTH, GRAPHICS, TICKS, TICK_MS, PAUSE, canvas, color, firstCars
    global lastCars, cars, SIM_LENGTH, GRAPHICS, CAR_PER_MIN, carcolor, autonomouscolor, buffercolor, TPS
    global EXPECTED_FINISHED, ROAD_MILES
    tk = Toplevel(root)
    # As of now, these 4 inputs dictate the simulation. LANE_HEIGHT is the pixel height of lanes, and car sizes will adjust accordingly.
    ROAD_LENGTH = tk.winfo_screenwidth()*19/20
    HEIGHT = tk.winfo_screenheight()/2
    LANE_COUNT = laneNum
    LANE_HEIGHT = 18 #round(HEIGHT/(LANE_COUNT*3),0)
    DEBUG = debug
    TICKS_UNTIL_ANIM = tickstilanim
    SIM_LENGTH = simlength
    GRAPHICS = graphics
    CAR_PER_MIN = carsPerMin
    if(not GRAPHICS):
        TICKS_UNTIL_ANIM = SIM_LENGTH

    WIDTH = ROAD_LENGTH
    CAR_SIZE = LANE_HEIGHT
    ROAD_FEET = ROAD_LENGTH / CAR_SIZE * 15.8
    ROAD_MILES = ROAD_FEET / 5280
    # This is how many pixels forward each car should move on a tick if they want to go speedlim MPH, assuming 100Ticks/ Sec
    SPEED_RMPH = ROAD_LENGTH / ROAD_MILES * speedlim / 60 / 60 / 100
    G_COUNT = 0
    ID_COUNTER = 0
    INSERT_LENGTH = CAR_SIZE * 2.0
    GRAPHICS = False
    TICKS = 0
    TICK_MS = 10
    PAUSE = False
    px = None
    py = None
    DEBUG_LABEL = None
    DEBUG_TEXT = None
    
    TPS = ROAD_MILES / (speedlim / 60.0 / 60.0 / 100.0)
    EXPECTED_FINISHED = carsPerMin / 60.0 / 100.0 * (simlength - TPS)
    EXPECTED_FINISHED = max(0.0, EXPECTED_FINISHED)

    canvas = None
    color = 'red'
    carcolor = 'red'
    autonomouscolor = 'blue'
    buffercolor = 'purple'
    firstCars = None
    lastCars = None
    cars = None
