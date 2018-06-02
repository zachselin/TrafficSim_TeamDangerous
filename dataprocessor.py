import numpy as np
import matplotlib.pyplot as plt
import os
import platform

class DataProcessor:

    def __init__(self, r):
        self.r = r
        self.session_data = []

    def process(self):
        r = self.getAvgs()
        self.session_data.append(r)
        
        # NOW USE THE DATA
        
        # RIGHT NOW I AM WRITING THIS AS A STRING TO A FILE. WE HAVE TO MANUALLY
        # COPY-PASTE THAT DATA INTO THINGS TO PLOT THEM. OTHERWISE WE DON'T KNOW
        # WHAT WE WANT FOR OUR PLOT
        f = None
        if(platform.system() == "Windows"):
            f = open(str(os.path.dirname(os.path.realpath(__file__))) + "\\analysis_data.txt", "a")
        else:
            f = open(str(os.path.dirname(os.path.realpath(__file__))) + "/analysis_data.txt", "a")
        f.write(str(r) + "\n\n")
        f.close()
        
        print("FILE LOCATION: " + str(os.path.dirname(os.path.realpath(__file__))))
        
        
        
    def getAvgs(self):
        sims = len(self.r)
        
        input_cars = []
        finished_cars = []
        ticks = []
        
        # extract single values
        attempted_avg = self.r[0]["attempted_input"]
        expected_avg = self.r[0]["expected_finished"]
        lanes_avg = self.r[0]["lanes"]
        sim_len_avg = self.r[0]["sim_len"]
        road_miles_avg = self.r[0]["road_miles"]
        perc_nc_avg = self.r[0]["perc_nc"]
        perc_bb_avg = self.r[0]["perc_bb"]
        perc_ac_avg = self.r[0]["perc_ac"]
        
        # extract from results
        idx = 0
        for s in self.r:
            input_cars.append(s["input_cars"])
            finished_cars.append(s["finished_cars"])
            ticks.append(np.array(s["speed_range_ticks"]))
            idx += 1
        
        input_avg = np.array(input_cars).mean()
        finished_avg = np.array(finished_cars).mean()
        ticks_avg = np.array(ticks).mean(axis=0)
        
        sr = {"lanes" : lanes_avg,
            "sim_len" : sim_len_avg,
            "road_miles" : road_miles_avg,
            "perc_nc" : perc_nc_avg,
            "perc_bb" : perc_bb_avg,
            "perc_ac" : perc_ac_avg,
            "attempted_input" : attempted_avg, 
            "input_cars" : input_avg, 
            "finished_cars" : finished_avg, 
            "expected_finished" : expected_avg,
            "speed_range_ticks" : ticks_avg}
        print("PERCENTAGE CALCULATED RESULTS: \n" + str(sr) + "\n")
        return sr
        