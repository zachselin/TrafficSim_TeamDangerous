import tkinter as tk
from tkinter import messagebox
import simulation as s
from tkinter.ttk import Progressbar
import time

class StartUI:

    simSize = 10
    simCancel = False
    simNumber = None
    root = None
    # variables for the checkbuttons
    boolDebug = None
    boolGraphics = None
    boolNormCar = None
    boolBBCar = None
    boolAutoCar = None
    sbNorm = None
    sbBBCar = None
    sbAuton = None
    cbNorm = None
    cbBBCar = None
    cbAuton = None
    lanes = 4
    speedLim = 60
    carsPerMin = 25
    numSim = 100
    simLength = 5000
    values = []
    
    def __init__(self):
        # Creating the window to hold all the items
        self.root = tk.Tk()
        self.root.title("Traffic Sim")
        # Changes the protocol for the 'x' button at the top of the window
        self.root.protocol('WM_DELETE_WINDOW', self.quit)

        self.boolDebug = tk.BooleanVar()
        self.boolGraphics = tk.BooleanVar()
        
        # gets the system screen size
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
              
        # creates a window based off the screen size
        winH = int(height*55/80)
        winW = int(width/3)
        
        # creates a string for tkinter to understand the window size
        size = "%dx%d" % (winW, winH)       
        self.root.geometry(size)
        
        self.boolDebug = tk.BooleanVar()
        self.boolGraphics = tk.BooleanVar()
        self.boolNormCar = tk.BooleanVar()
        self.boolBBCar = tk.BooleanVar()
        self.boolAutoCar = tk.BooleanVar()
        
        # creates a container for all items in the window
        content = tk.Frame(self.root)
        content.grid(column = 0, row = 0)
        
        # creates a frame on the left side of the content container for all changing variables and buttons
        frame = tk.Frame(content, bg = "white", height = winH, width = winW*4/5)
        frame.grid(column = 0, columnspan = 4, row = 0, rowspan = 8, sticky = ('n', 's', 'w'))
        
        
        # Creates trays inside the frame, one for heading (ftTray), one for sliders (sTray), one for additional settings (fbTray)
        ftTray = tk.Frame(frame, bg = 'light grey', height = winH/8, width = winW*4/5)
        sTray = tk.Frame(frame, bg = 'white', height = winH*5/8, width = winW*4/5)
        fbTray = tk.Frame(frame, bg = 'light grey', height = winH*2/8, width = winW*4/5)
        ftTray.grid(column = 0, columnspan = 4, row = 0, rowspan = 1)
        sTray.grid(column = 0, columnspan = 4, row = 1, rowspan = 5)
        fbTray.grid(column = 0, columnspan = 4, row = 6, rowspan = 2, pady = 10)
        
        #Labels and Sliders for variables for the sim
        laneLabel = tk.Label(sTray, text = 'Number of Lanes:', bg = 'white')
        laneLabel.grid(column = 0, row = 0, sticky = 'w')
        self.lanes = tk.Scale(sTray, from_ = 2, to = 10, orient = 'horizontal', length = winH*3/5, resolution = 1)
        self.lanes.grid(column = 0, row = 1, padx = 15, pady = 10)
        self.lanes.set(5)
        
        speedLabel = tk.Label(sTray, text = 'Speed Limit (in MPH):', bg = 'white')
        speedLabel.grid(column = 0, row = 3, sticky = 'w')
        self.speedLim = tk.Scale(sTray, from_ = 25, to = 70, orient = 'horizontal', length = winH*3/5, resolution = 5)
        self.speedLim.grid(column = 0, row = 4, padx = 15, pady = 10)
        self.speedLim.set(60)
        
        cpmLabel = tk.Label(sTray, text = 'Cars per Minute:', bg = 'white')
        cpmLabel.grid(column = 0, row = 5, sticky = 'w')
        self.carsPerMin = tk.Scale(sTray, from_ = 50, to = 1400, orient = 'horizontal', length = winH*3/5, resolution = 10)
        self.carsPerMin.grid(column = 0, row = 6, padx = 15, pady = 10)
        self.carsPerMin.set(300)
        
        numSimLabel = tk.Label(sTray, text = 'Number of Simulations:', bg = 'white')
        numSimLabel.grid(column = 0, row = 7, sticky = 'w')
        self.numSim = tk.Scale(sTray, from_ = 10, to = 10000, orient = 'horizontal', length = winH*3/5, resolution = 10)
        self.numSim.grid(column = 0, row = 8, padx = 15, pady = 10)
        self.numSim.set(10)
        
        simLenLabel = tk.Label(sTray, text = 'Simulation Length (in ticks):', bg = 'white')
        simLenLabel.grid(column = 0, row = 9, sticky = 'w')
        self.simLength = tk.Scale(sTray, from_ = 1000, to = 100000, orient = 'horizontal', length = winH*3/5, resolution = 1000)
        self.simLength.grid(column = 0, row = 10, padx = 15, pady = 10)
        self.simLength.set(3000)

        #Label for the top tray
        mainLabel = tk.Label(ftTray, text = 'Traffic Simulator', bg = 'white')
        mainLabel.grid(column = 0, row = 0)
        
        # creates check buttons for specific settings for the simulation
        self.cbNorm = tk.Checkbutton(fbTray, bg = 'light grey', text = 'Enable Normal Cars', variable = self.boolNormCar, command = self.NormalCar)
        self.cbBBCar = tk.Checkbutton(fbTray, bg = 'light grey', text = 'Enable Buffer Builders', variable = self.boolBBCar, command = self.BBCar)
        self.cbAuton = tk.Checkbutton(fbTray, bg = 'light grey', text = 'Enable Autonomus Cars', variable = self.boolAutoCar, command = self.AutoCar)
        self.cbNorm.grid(column = 0, row = 0, sticky = 'w')
        self.cbBBCar.grid(column = 0, row = 1, sticky = 'w')
        self.cbAuton.grid(column = 0, row = 2, sticky = 'w')    
        self.cbNorm.toggle()
        self.boolNormCar.set(True)
        
        self.sbNorm = tk.Spinbox(fbTray, from_=0, to= 100, width = 3, increment = 5, wrap = True, command = self.changeNorm)
        self.sbBBCar = tk.Spinbox(fbTray, from_=0, to= 100, width = 3, increment = 5, wrap = True, command = self.changeBBCar)
        self.sbAuton = tk.Spinbox(fbTray, from_=0, to= 100, width = 3, increment = 5, wrap = True, command = self.changeAuto)
        self.sbNorm.grid(column = 1, row = 0, sticky = 'e', padx = 30)
        self.sbBBCar.grid(column = 1, row = 1, sticky = 'e', padx = 30)
        self.sbAuton.grid(column = 1, row = 2, sticky = 'e', padx = 30)
        self.sbNorm.invoke('buttondown')
        self.sbNorm['state'] = 'readonly'
        self.sbBBCar['state'] = 'disable'
        self.sbAuton['state'] = 'disable'
        
        
        
        # creates a button tray
        rTray = tk.Frame(content, bg = "grey", height = winH, width = winW/5)
        rTray.grid(column = 4, columnspan = 1, row = 0, rowspan = 8, sticky = ('n', 's', 'e'))
        
        # creates a right side tray
        bTray = tk.Frame(rTray, bg = 'light gray', height = winH*3/8, width = winW/5)
        bTray.grid(column = 0, columnspan = 2, row = 0, rowspan = 4, sticky = 'n')
        
        # Label for the functions
        functLabel = tk.Label(bTray, text = 'Functions')
        functLabel.grid(column = 0, row = 0, sticky = ('n', 'w', 'e'))
        
        # buttons to make sim work
        cbDebug = tk.Checkbutton(bTray, bg = "light grey", text = 'Enable Debugging', variable = self.boolDebug, command = self.debugWarning)
        cbGraphics = tk.Checkbutton(bTray, bg = "light grey", text = 'Enable Graphics', variable = self.boolGraphics, command = self.graphicsCheck)
        bRun = tk.Button(bTray, text = "Run", command = self.run)
        bQuit = tk.Button(rTray, text = 'Quit', command = self.quit)
        bRun.grid(column = 0, columnspan = 2,row = 1, padx = 15, pady = 15)
        bQuit.grid(column = 0, columnspan = 2,row = 7)
        cbDebug.grid(column = 0, row = 2, sticky = 'w')
        cbGraphics.grid(column = 0, row = 3, sticky = 'w')
        
        # configures for buttons and labels
        functLabel.config(width = int(winW*4/12/10))
        bRun.config(width = 10)
        bQuit.config(width = 10)
        
        
        # configs for window itself
        self.root.columnconfigure(0, weight = 1)
        self.root.rowconfigure(0, weight = 1)
        
        # configs for the content container
        content.columnconfigure(0, weight = 1)
        content.columnconfigure(1, weight = 1)
        content.columnconfigure(2, weight = 1)
        content.columnconfigure(3, weight = 1)
        content.columnconfigure(4, weight = 1)
        content.rowconfigure(0, weight = 1)
        
        # configs for the frame container
        frame.columnconfigure(0, weight = 1)
        frame.columnconfigure(1, weight = 1)
        frame.columnconfigure(2, weight = 1)
        frame.columnconfigure(3, weight = 1)
        frame.columnconfigure(4, weight = 1)
        frame.columnconfigure(5, weight = 1)
        frame.rowconfigure(0, weight = 1)
        frame.rowconfigure(1, weight = 1)
        frame.rowconfigure(2, weight = 1)
        frame.rowconfigure(3, weight = 1)
        frame.rowconfigure(4, weight = 1)
        frame.rowconfigure(5, weight = 1)
        frame.rowconfigure(6, weight = 1)
        frame.rowconfigure(7, weight = 1)
        
        # configs for the right tray
        rTray.columnconfigure(0, weight = 1)
        rTray.columnconfigure(1, weight = 1)
        rTray.rowconfigure(0, weight = 1)
        rTray.rowconfigure(1, weight = 1)
        rTray.rowconfigure(2, weight = 1)
        rTray.rowconfigure(3, weight = 1)
        rTray.rowconfigure(4, weight = 1)
        rTray.rowconfigure(5, weight = 1)
        rTray.rowconfigure(6, weight = 1)
        rTray.rowconfigure(7, weight = 1)
        
        self.root.mainloop()
        return None
        
    # the function for running the simulation
    def run(self):
        # sets the initial values of things
        self.simCancel = False
        tempvalues = []
        
        # creates a new window for the progress bar and other buttons
        self.progWin = tk.Toplevel(self.root)
        self.progWin.title("SimulationRun")
        self.progWin.protocol('WM_DELETE_WINDOW', self.cancel)
        
        # creates a style for the progress bar
        style = tk.ttk.Style()
        style.theme_use('default')
        style.configure("black.Horizontal.TProgressbar", background='black')
        
        # makes lable for the progress meter
        progLabel = tk.Label(self.progWin, text = 'Simulation Progress:')
        progLabel.grid(column = 0, row = 0, sticky = 'w')
        
        # makes a lable for current progress percent
        curProgLabel = tk.Label(self.progWin, text= '0.00%')
        curProgLabel.grid(column = 1, row = 0, sticky = 'w')
        
        timeLabel = tk.Label(self.progWin, text = 'Estimated Time Remaining:')
        timeLabel.grid(column = 0, row = 2, sticky = 'w')
        
        timeRemain = tk.Label(self.progWin, text = 'HRS:MIN:SEC')
        timeRemain.grid(column = 1, row = 2, sticky = 'w')
        
        # makes a progress bar set to just under the size of the window
        bar = Progressbar(self.progWin, length = self.root.winfo_screenwidth()/5, style = 'black.Horizontal.TProgressbar')  
        bar.grid(column = 0, columnspan = 4, row = 1, padx = 10, pady = 5)
        
        # Creates buttons for cancal and analyse
        bCancel = tk.Button(self.progWin, text = 'Cancel', command = self.cancel)
        bCancel.grid(column = 1, row = 3, pady = 5)
        bAnalyse = tk.Button(self.progWin, text = 'Analyse', command = lambda: self.analyse(tempvalues))
        bAnalyse['state'] = 'disable'
        bAnalyse.grid(column = 0, row = 3, pady = 5)

        # updates window
        self.progWin.update()
        
        #gets sim number
        self.simNumber = self.numSim.get()
        
        # gets sim length
        simLen = self.simLength.get()
        
        # gets car ratios
        ratioNC = int(self.sbNorm.get())
        ratioBB = int(self.sbBBCar.get())
        ratioAC = int(self.sbAuton.get())
        
        # validity checks for different data fields
        if(not self.boolNormCar.get() or ratioNC < 0):
            ratioNC = 0
            
        if(not self.boolBBCar.get() or ratioBB < 0):
            ratioBB = 0
            
        if(not self.boolAutoCar.get() or ratioAC < 0):
            ratioAC = 0
        
        if(self.boolGraphics.get()):
            self.simNumber = 1
            simLen = 100000
            
        # counter for tests
        simiters = 0.0
        # runs the tests
        for i in range(self.simNumber):
            # checks if the sim should still run
            if(self.simCancel == True):
                self.progWin.quit()
                messagebox.showwarning('Sim Canceled', 'Simulation has been interrupted.')
                return
                
            self.sim = s.simulator(self.root, self.lanes.get(), self.boolDebug.get(),
                                    self.speedLim.get(), self.boolGraphics.get(),
                                    simLen, 8, self.carsPerMin.get(), ratioNC, ratioBB,
                                    ratioAC, False)
            t0 = time.time()
            self.sim.start()
            t1 = time.time()
            deltaT = t1 - t0
            estTime = round((self.simNumber -simiters) * deltaT, 2)
           
            sec = round(estTime % 60)
            min = int((estTime - sec) / 60) % 60
            hr = int(estTime/60/60)
            timeStr = ''
            
            if(hr > 0):
                timeStr += str(hr) + " Hours "
                
            if(min > 0): 
                timeStr += str(min) + " Minutes "
                
            timeStr += str(sec) + " Seconds"
            
            timeRemain['text'] = str(timeStr)

            self.sim.collect_results()
            tempvalues.append(self.sim.RESULTS)
            simiters += 1.0
            bar['value'] = round(simiters / float(self.simNumber) * 100.0, 2)
           
            if(round(simiters / float(self.simNumber) * 100.0, 2) == 100):
                timeRemain['text'] = 'Done'   
            curProgLabel['text'] = str(bar['value']) + "%"
            self.progWin.update()
            
            

        bCancel['state'] = 'disable'
        bAnalyse['state'] = 'normal'
        
        
    def graphicsCheck(self):
        if(not self.boolGraphics.get()):
            messagebox.showwarning('Graphics Enabled','Enabling Graphics will limit\n number of simulations to 1.')
            self.boolGraphics.set(True)
            self.numSim['state'] = 'disable'
            
        else:
            self.boolGraphics.set(False)
            self.numSim['state'] = 'normal'
            
            
    def debugWarning(self):
        if(not self.boolDebug.get()):
            messagebox.showwarning('Debugging Enabled','Debugging will slow down the simulation\n speed and may cause the system to crash.')
            self.boolDebug.set(True)
        else:
            self.boolDebug.set(False)
            
    def cancel(self):
        self.simCancel = messagebox.askyesno('Cancel Sim','Do you want to cancel the sim?')
        if(self.simCancel == True):
            self.progWin.destroy()    
            return

    # method for analysing the data            
    def analyse(self, values):
        self.values = values
        self.progWin.destroy()
        print(values)
        
    # Method for quiting the application   
    def quit(self):
        quit = messagebox.askokcancel('Quit','Quitting simulation.')
        if(quit):
            self.root.destroy()
            self.root.quit()
        else: return
    
    # Method for changing the values in the spin boxes so they always equal 100
    def changeNorm(self):
        # Checks if the percent of norm now is above the remainer of the bb car and auto car percent from 100
        if(int(self.sbNorm.get()) > 100 - int(self.sbBBCar.get()) - int(self.sbAuton.get())):
            
            #Checks if BB Car is enabled, if so changes the bbCar to the remainder of 100 - norm - auto
            if(self.boolBBCar.get() and int(self.sbBBCar.get()) > 0):
                self.sbBBCar['state'] = 'normal'
                self.sbBBCar.delete(0, 'end')
                self.sbBBCar.insert(0, 100 - int(self.sbNorm.get()) - int(self.sbAuton.get()))
                self.sbBBCar['state'] = 'readonly'
            
            #Checks if auto Car is enabled, if so changes the Auto to remainder of 100 - norm
            elif(self.boolAutoCar.get()):
                self.sbAuton['state'] = 'normal'
                self.sbAuton.delete(0, 'end')
                self.sbAuton.insert(0, 100 - int(self.sbNorm.get()))
                self.sbAuton['state'] = 'readonly'
              
        # else sets the value of the spin box to the remainder of 100 - bb car - auto car
        else:
            self.sbNorm['state'] = 'normal'
            self.sbNorm.delete(0,"end")
            self.sbNorm.insert(0,100 - int(self.sbBBCar.get()) - int(self.sbAuton.get()))
            self.sbNorm['state'] = 'readonly'
    
    # Method for changing the values in the spin boxes so they always equal 100
    def changeBBCar(self):
        # Checks if the percent of bb car now is above the remainer of the norm and auto car percent from 100
        if(int(self.sbBBCar.get()) > 100 - int(self.sbNorm.get()) - int(self.sbAuton.get())):
            
            #Checks if Norm is enabled, if so changes the bbCar to the remainder of 100 - bb car - auto
            if(self.boolNormCar.get() and int(self.sbNorm.get()) > 0):    
                self.sbNorm['state'] = 'normal'
                self.sbNorm.delete(0, 'end')
                self.sbNorm.insert(0, 100 - int(self.sbBBCar.get()) - int(self.sbAuton.get()))
                self.sbNorm['state'] = 'readonly'
            
            #Checks if auto Car is enabled, if so changes the Auto to remainder of 100 - norm
            elif(self.boolAutoCar.get()):
                self.sbAuton['state'] = 'normal'
                self.sbAuton.delete(0, 'end')
                self.sbAuton.insert(0, 100 - int(self.sbBBCar.get()))
                self.sbAuton['state'] = 'readonly'
              
        
        # else sets the value of the spin box to the remainder of 100 - norm - auto car
        else:
            self.sbBBCar['state'] = 'normal'
            self.sbBBCar.delete(0,"end")
            self.sbBBCar.insert(0,100 - int(self.sbNorm.get()) - int(self.sbAuton.get()))
            self.sbBBCar['state'] = 'readonly'
            
    # Method for changing the values in the spin boxes so they always equal 100        
    def changeAuto(self):
        # Checks if the percent of auto car is above the remainer of the bb car and norm percent from 100
        if(int(self.sbAuton.get()) > 100 - int(self.sbNorm.get()) - int(self.sbBBCar.get())):
            
            #Checks if Norm is enabled, if so changes the norm to the remainder of 100 - bb car - auto
            if(self.boolNormCar.get() and int(self.sbNorm.get()) > 0):
                self.sbNorm['state'] = 'normal'
                self.sbNorm.delete(0, 'end')
                self.sbNorm.insert(0, 100 - int(self.sbBBCar.get()) - int(self.sbAuton.get()))
                self.sbNorm['state'] = 'readonly'
            
            #Checks if bb Car is enabled, if so changes the bb car to remainder of 100 - auto
            elif(self.boolAutoCar.get()):
                self.sbBBCar['state'] = 'normal'
                self.sbBBCar.delete(0, 'end')
                self.sbBBCar.insert(0, 100 - int(self.sbAuton.get()))
                self.sbBBCar['state'] = 'readonly'
              
        
        # else sets the value of the spin box to the remainder of 100 - norm - auto car
        else:
            self.sbAuton['state'] = 'normal'
            self.sbAuton.delete(0,"end")
            self.sbAuton.insert(0,100 - int(self.sbNorm.get()) - int(self.sbBBCar.get()))
            self.sbAuton['state'] = 'readonly'
            
        
    # method for updating the spin box based on checkbox selection for the Normal Car
    def NormalCar(self):
        # checks if other car types are enabled, if not then displays a warning
        if(not self.boolBBCar.get() and not self.boolAutoCar.get()):
            self.cbNorm.select()
            messagebox.showwarning('Sim warning', 'One type of car must be enabled')
            
        #Checks if the button is currently disabled, if so, enables button
        elif(not self.boolNormCar.get()):
            self.boolNormCar.set(True)
            self.sbNorm['state'] = 'readonly'            
        
        #Else disables button
        else:
            self.sbNorm['state'] = 'normal'
            #Checks if BB Car is enabled, if so moves the percent in Norm to BB Car
            if(self.boolBBCar.get()):
                self.sbBBCar['state'] = 'normal'
                bbCar = int(self.sbBBCar.get())
                self.sbBBCar.delete(0, 'end')
                self.sbBBCar.insert(0, bbCar + int(self.sbNorm.get()))
                self.sbBBCar['state'] = 'readonly'
            
            #Checks if auto Car is enabled, if so moves the percent in Norm to Auto
            elif(self.boolAutoCar.get()):
                self.sbAuton['state'] = 'normal'
                auto = int(self.sbAuton.get())
                self.sbAuton.delete(0, 'end')
                self.sbAuton.insert(0, auto + int(self.sbNorm.get()))
                self.sbAuton['state'] = 'readonly'
        
            # Sets auto car to 0 
            self.sbNorm.delete(0, 'end')
            self.sbNorm.insert(0, '0')
        
            # disables button and sets bool flag to false
            self.boolNormCar.set(False)
            self.sbNorm['state'] = 'disable'
                
                
    # method for updating the spin box based on checkbox selection for the Buffer Car
    def BBCar(self):
        # checks if other car types are enabled, if not then displays a warning
        if(not self.boolNormCar.get() and not self.boolAutoCar.get()):
            self.cbBBCar.select()
            messagebox.showwarning('Sim warning', 'One type of car must be enabled')
            
        #Checks if the button is currently disabled, if so, enables button
        elif(not self.boolBBCar.get()):
            self.boolBBCar.set(True)
            self.sbBBCar['state'] = 'readonly'
        
        #Else disables button
        else:
            self.sbBBCar['state'] = 'normal'
            #Checks if normal car is enabled, if so moves the percent in BB Car to Normal Car
            if(self.boolNormCar.get()):
                self.sbNorm['state'] = 'normal'
                norm = int(self.sbNorm.get())
                self.sbNorm.delete(0, 'end')
                self.sbNorm.insert(0, norm + int(self.sbBBCar.get()))
                self.sbNorm['state'] = 'readonly'
                
            #Checks if auto Car is enabled, if so moves the percent in BB Car to Auto
            elif(self.boolAutoCar.get()):
                self.sbAuton['state'] = 'normal'
                auto = int(self.sbAuton.get())
                self.sbAuton.delete(0, 'end')
                self.sbAuton.insert(0, auto + int(self.sbBBCar.get()))
                self.sbAuton['state'] = 'readonly'
        
            # Sets auto car to 0 
            self.sbBBCar.delete(0, 'end')
            self.sbBBCar.insert(0, '0') 
            
            # disables button and sets bool flag to false
            self.boolBBCar.set(False)
            self.sbBBCar['state'] = 'disable'
                
    
    # method for updating the spin box based on checkbox selection for the Autonomus Car
    def AutoCar(self):
        # checks if other car types are enabled, if not then displays a warning
        if(not self.boolBBCar.get() and not self.boolNormCar.get()):
            self.cbAuton.select()
            messagebox.showwarning('Sim warning', 'One type of car must be enabled')
            
        #Checks if the button is currently disabled, if so, enables button
        elif(not self.boolAutoCar.get()):
            self.boolAutoCar.set(True)
            self.sbAuton['state'] = 'readonly'
            
        #Else disables button
        else:
            self.sbAuton['state'] = 'normal'
            #Checks if normal car is enabled, if so moves the percent in Auto to Normal Car
            if(self.boolNormCar.get()):
                self.sbNorm['state'] = 'normal'
                norm = int(self.sbNorm.get())
                self.sbNorm.delete(0, 'end')
                self.sbNorm.insert(0, norm + int(self.sbAuton.get()))
                self.sbNorm['state'] = 'readonly'
            
            #Checks if BB Car is enabled, if so moves the percent in Auto to BB Car
            elif(self.boolBBCar.get()):
                self.sbBBCar['state'] = 'normal'
                bbCar = int(self.sbBBCar.get())
                self.sbBBCar.delete(0, 'end')
                self.sbBBCar.insert(0, bbCar + int(self.sbAuton.get()))
                self.sbBBCar['state'] = 'readonly'
                
            # Sets auto car to 0
            self.sbAuton.delete(0, 'end')
            self.sbAuton.insert(0, '0')    
            
            # disables button and sets bool flag to false
            self.boolAutoCar.set(False)
            self.sbAuton['state'] = 'disable'  
        
app = StartUI()
