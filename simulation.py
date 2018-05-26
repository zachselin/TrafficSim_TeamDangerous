import shared as g
from car import Car
import numpy as np

class simulator:
    debug = False
    def __init__(self, laneNum, debug, speedlim, graphics, simlength):
        g.init_vals(laneNum, debug, speedlim, graphics, simlength)
        self.init_data_structs()
            
    def init_data_structs(self):
        g.tk.bind("<space>", self.pause)
        g.cars = []
        for i in range(g.LANE_COUNT):
            g.cars.append([])
    
    def init_lanes(self):
        g.canvas = g.Canvas(g.tk, width=g.WIDTH, height=g.HEIGHT, bg="green")
        g.canvas.create_line(0, (g.HEIGHT / 2), g.WIDTH, (g.HEIGHT / 2), width=str(g.LANE_HEIGHT * g.LANE_COUNT), fill="grey")
        g.canvas.pack()
        for lane in range(g.LANE_COUNT+1):
            line_thickness = (1, 3)[lane == 0 or lane == g.LANE_COUNT]
            g.canvas.create_line(0, (g.HEIGHT/2) + g.LANE_HEIGHT*(lane-(g.LANE_COUNT/2.0)), g.WIDTH, (g.HEIGHT/2) + g.LANE_HEIGHT*(lane-(g.LANE_COUNT/2.0)),
                            width=str(line_thickness), fill="white")
    
    def init_debug_text(self):
        g.DEBUG_TEXT = g.StringVar()
        g.DEBUG_LABEL = g.Label(g.tk, textvariable=g.DEBUG_TEXT, font="Times 10").pack()
    
    def init_anim(self):
        self.init_lanes()
        if(self.debug):
            self.init_debug_text()
        for lane in g.cars:
            for car in lane:
                car.setup_visual(g.canvas)
            g.ANIMATION = True
    
    def make_car(self):
        lane = np.random.randint(1, g.LANE_COUNT+1)
        if(len(g.cars[lane-1]) == 0 or g.cars[lane-1][-1].posx > g.INSERT_LENGTH):
            speed = np.random.uniform(.5*g.SPEED_MOD, 1*g.SPEED_MOD)
            # reference to ahead cars
            carUpAhead = None
            carDownAhead = None
            carAhead = None
            if(len(g.cars[lane-1]) > 0):
                carAhead = g.cars[lane-1][-1]
            if(lane > 1 and len(g.cars[lane-2]) > 0):
                carUpAhead = g.cars[lane-2][-1]
            else:
                carUpAhead = None
            if(lane < g.LANE_COUNT and len(g.cars[lane]) > 0):
                carDownAhead = g.cars[lane][-1]
            car = Car(lane, speed, g.ID_COUNTER, carAhead, carUpAhead, carDownAhead, len(g.cars[lane-1]), g.CAR_SIZE, g.HEIGHT, g.LANE_COUNT) # last param is index in lane list
            if(g.ANIMATION):
                car.setup_visual(g.canvas)
            g.ID_COUNTER += 1
            g.cars[lane-1].append(car)
    
    def pause(self, event):
        g.PAUSE = (not g.PAUSE)
    
    def tick(self):
        g.px = g.tk.winfo_pointerx() - g.tk.winfo_rootx()
        g.py = g.tk.winfo_pointery() - g.tk.winfo_rooty()
        if(g.TICKS % 20 == 0):
            self.make_car()
        if(not g.PAUSE):
            for lane in g.cars:
                for car in lane:
                    car.move_active()
            #for lane in g.cars:
            #    for car in lane:
            #        car.ensure_references()
        if(g.ANIMATION and not g.PAUSE):
            for lane in g.cars:
                for car in lane:
                    car.update_anim()
        if(g.DEBUG_REFERENTIAL):
            for lane in g.cars:
                for car in lane:
                    car.debug()
        g.TICKS += 1
    
    def control(self):
        self.tick()
        g.tk.after(g.TICK_MS, self.control)
        
    def start(self):
        for ism in range(g.SIM_LENGTH):
            for it in range(g.TICKS_UNTIL_ANIM):
                self.tick()
            self.init_anim()
            self.control()
            g.tk.update()
        