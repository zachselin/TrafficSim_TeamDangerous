import shared as g
from car import Car
from autonomouscar import Autonomous
import math
import numpy as np
import time
import random

class simulator:
    def __init__(self, root, laneNum, debug, speedlim, graphics, simlength, tickstilanim, carsPerMin, ratioNC, ratioBB, ratioAC):
        # these variables are necessary to track sim outcome data and data to run multiple sims
        self.ROOT = root
        self.DONE = False
        self.DEBUG = debug
        self.CAR_PER_MIN = carsPerMin
        self.LANE_NUM = laneNum
        self.SPEED_LIM = speedlim
        self.GRAPHICS = graphics
        self.SIM_LEN = simlength
        self.ANIM_TICKS = tickstilanim
        self.CRASH = False
        self.RESULTS = []
        self.starttime = time.time()
        self.itertime = time.time()
        self.RNC = ratioNC
        self.RBB = ratioBB
        self.RAC = ratioAC

        # MAKE CARS DATA
        self.CARS_TO_MAKE = carsPerMin / 60.0 / 100.0 * simlength
        self.CARS_MADE = 0

        # RESULTS / ANALYTICS DATA
        self.rATTEMPTED_INPUT = self.CARS_TO_MAKE
        self.rFINISHED_CARS = 0
        self.rINPUT_CARS = 0
        self.rSPEED_RANGE_TICKS = [0, 0, 0, 0, 0]
        
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
        if(g.DEBUG):
            self.init_debug_text()
        for lane in g.cars:
            for car in lane:
                car.setup_visual(g.canvas)
            g.GRAPHICS = True
    
    def make_car(self):
        lanes = list(range(1, self.LANE_NUM+1))
        random.shuffle(lanes)
        #print("lanes: " + str(lanes))
        for l in lanes:
            if (len(g.cars[l - 1]) == 0 or g.cars[l - 1][-1].posx > g.INSERT_LENGTH):
                self.rINPUT_CARS += 1
                speed = np.random.uniform(.5 * g.SPEED_RMPH, 1 * g.SPEED_RMPH)
                # reference to ahead cars
                carUpAhead = None
                carDownAhead = None
                carAhead = None
                if (len(g.cars[l - 1]) > 0):
                    carAhead = g.cars[l - 1][-1]
                if (l > 1 and len(g.cars[l - 2]) > 0):
                    carUpAhead = g.cars[l - 2][-1]
                else:
                    carUpAhead = None
                if (l < g.LANE_COUNT and len(g.cars[l]) > 0):
                    carDownAhead = g.cars[l][-1]
                indivSpeed = np.random.normal(g.SPEED_RMPH * 1.05, 1.0)
                car = Car(self, l, speed, g.SPEED_RMPH, g.ID_COUNTER, carAhead, carUpAhead, carDownAhead,
                          len(g.cars[l - 1]), g.CAR_SIZE, g.HEIGHT, g.LANE_COUNT)  # last param is index in lane list
                if (g.GRAPHICS):
                    car.setup_visual(g.canvas)
                g.ID_COUNTER += 1
                g.cars[l - 1].append(car)
                self.CARS_MADE += 1
                return

    def make_cars(self):
        expected_made = math.ceil(g.TICKS / self.SIM_LEN * self.CARS_TO_MAKE)
        #print("expected made: " + str(g.TICKS / self.SIM_LEN * self.CARS_TO_MAKE))
        #print("Ticks: " + str(g.TICKS))
        if(self.CARS_MADE < expected_made):
            self.make_car()


    def car_delete(self, car):
        self.rFINISHED_CARS += 1
        del(car)

    def collect_results(self):
        t = self.rSPEED_RANGE_TICKS
        total_ticks = t[0] + t[1] + t[2] + t[3] + t[4]
        self.RESULTS = {
            "attempted_input" : self.rATTEMPTED_INPUT,
            "input_cars" : self.rINPUT_CARS,
            "finished_cars" : self.rFINISHED_CARS,
            "speed_range_ticks" : self.rSPEED_RANGE_TICKS
        }
    
    def pause(self, event):
        g.PAUSE = (not g.PAUSE)
    
    def tick(self):
        g.px = g.tk.winfo_pointerx() - g.tk.winfo_rootx()
        g.py = g.tk.winfo_pointery() - g.tk.winfo_rooty()
        self.make_cars()
        #if(g.TICKS % 20 == 0):
        #    self.make_car()
        if(not g.PAUSE):
            for lane in g.cars:
                for car in lane:
                    car.move_active()
            #for lane in g.cars:
            #    for car in lane:
            #        car.ensure_references()
        if(g.GRAPHICS and not g.PAUSE):
            for lane in g.cars:
                for car in lane:
                    car.update_anim()
        if(g.DEBUG):
            for lane in g.cars:
                for car in lane:
                    car.debug()
        if(not g.PAUSE):
            g.TICKS += 1
    
    def control(self):
        self.tick()
        if(g.TICKS <= self.SIM_LEN):
            g.tk.after(g.TICK_MS, self.control)
        else:
            self.DONE = True
            if(g.GRAPHICS):
                g.tk.quit()
            g.tk.destroy()
            #print("iter time: " + str(time.time() - self.itertime))
            #print("total time: " + str(time.time() - self.starttime))
        
        
    def start(self):
        # PUT ALL ANALYTICS INTO results
        results = []
        self.start_indiv_sim()
        while(not self.DONE):
            time.sleep(0.2)
        #g.tk.destroy()
        # BUILD ANALYTICS OBJECT, GIVE RESULTS AS PARAMETER
        return 100.0


    def start_indiv_sim(self):
        g.init_vals(self.ROOT, self.LANE_NUM, self.DEBUG, self.SPEED_LIM, self.GRAPHICS, self.SIM_LEN, self.ANIM_TICKS, self.CAR_PER_MIN)
        self.init_data_structs()
        for it in range(g.TICKS_UNTIL_ANIM):
            self.tick()
        if(g.TICKS <= g.TICKS_UNTIL_ANIM and g.TICKS < g.SIM_LENGTH):
            self.init_anim()
        self.control()
        if(g.GRAPHICS):
            g.tk.mainloop()
        
    def close(self):
        g.tk.destroy()
        g.tk.quit()




# TEST SIM FUNCTIONALITY SEPARATE FROM UI
import tkinter as tk
s = simulator(None, 2, True, 60, True, 5000, 200, 50, 100, 0, 0)
s.ROOT = tk.Tk()
s.start()
