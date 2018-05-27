from tkinter import *

def init_vals(laneNum, roadmiles, debug, speedlim, graphics, simlength, tickstilanim):
    global tk, ROAD_LENGTH, HEIGHT, LANE_HEIGHT, LANE_COUNT, DEBUG, TICKS_UNTIL_ANIM, WIDTH, CAR_SIZE
    global SPEED_RMPH, G_COUNT, ID_COUNTER, INSERT_LENGTH, GRAPHICS, TICKS, TICK_MS, PAUSE, canvas, color, firstCars
    global lastCars, cars, SIM_LENGTH, GRAPHICS, DEBUG_TEXT, DEBUG_LABEL
    tk = Tk()
    # As of now, these 4 inputs dictate the simulation. LANE_HEIGHT is the pixel height of lanes, and car sizes will adjust accordingly.
    ROAD_LENGTH = tk.winfo_screenwidth()*19/20
    HEIGHT = tk.winfo_screenheight()/2
    ROAD_MILES = roadmiles
    CAR_SIZE = tk.winfo_screenwidth() * 19 / 20 / ROAD_MILES * 15.8 / 5280
    print(roadmiles)
    print(str(CAR_SIZE))
    print("road len: " + str(ROAD_LENGTH))
    LANE_HEIGHT = CAR_SIZE
    LANE_COUNT = laneNum
    DEBUG = debug
    TICKS_UNTIL_ANIM = tickstilanim
    SIM_LENGTH = simlength
    GRAPHICS = graphics
    if(not GRAPHICS):
        TICKS_UNTIL_ANIM = SIM_LENGTH

    WIDTH = ROAD_LENGTH
    # This is how many pixels forward each car should move on a tick if they want to go speedlim MPH, assuming 100Ticks/ Sec
    SPEED_RMPH = ROAD_LENGTH / ROAD_MILES * speedlim / 60 / 60 / 100
    G_COUNT = 0
    ID_COUNTER = 0
    INSERT_LENGTH = CAR_SIZE / 2.0
    GRAPHICS = False
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


    MAX_ANIM_ROAD_MILES = tk.winfo_screenwidth()*19/20 / 4 * 15.8 / 5280
    #print("Max Road Miles (for animation): " + str(MAX_ANIM_ROAD_MILES))
