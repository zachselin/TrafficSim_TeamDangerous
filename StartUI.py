import tkinter as tk
from tkinter import messagebox
import simulation as s
from tkinter.ttk import Progressbar
import time

class StartUI:

    simSize = 10
    simCancel = False
    # variables for the checkbuttons
    #boolDebug = tk.BooleanVar()
    #boolGraphics = tk.BooleanVar()
    lanes = 4
    speedLim = 60
    carPerMinute = 25
    numSim = 100
    simLength = 5000
    values = []
    
    def __init__(self):
        # Creating the window to hold all the items
        self.window = tk.Tk()
        self.window.title("Traffic Sim")
        # Changes the protocol for the 'x' button at the top of the window
        self.window.protocol('WM_DELETE_WINDOW', self.quit)

        self.boolDebug = tk.BooleanVar()
        self.boolGraphics = tk.BooleanVar()
        
        # gets the system screen size
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
              
        # creates a window based off the screen size
        winH = int(height*51/80)
        winW = int(width/3)
        
        # creates a string for tkinter to understand the window size
        size = "%dx%d" % (winW, winH)       
        self.window.geometry(size)
        
        # creates a container for all items in the window
        content = tk.Frame(self.window)
        content.grid(column = 0, row = 0)
        
        # creates a frame on the left side of the content container for all changing variables and buttons
        frame = tk.Frame(content, bg = "white", height = winH, width = winW*4/5)
        frame.grid(column = 0, columnspan = 4, row = 0, rowspan = 8, sticky = ('n', 's', 'w'))
        

        # Creates trays inside the frame, one for heading (ftTray), one for sliders (sTray), one for additional settings (fbTray)
        ftTray = tk.Frame(frame, bg = 'white', height = winH/8, width = winW*4/5)
        sTray = tk.Frame(frame, bg = 'white', height = winH*5/8, width = winW*4/5)
        fbTray = tk.Frame(frame, bg = 'white', height = winH*2/8, width = winW*4/5)
        ftTray.grid(column = 0, columnspan = 4, row = 0, rowspan = 1)
        sTray.grid(column = 0, columnspan = 4, row = 1, rowspan = 5)
        fbTray.grid(column = 0, columnspan = 4, row = 6, rowspan = 2)
        
        #Labels and Sliders for variables for the sim
        laneLabel = tk.Label(sTray, text = 'Number of Lanes:', bg = 'white')
        laneLabel.grid(column = 0, row = 0, sticky = 'w')
        self.lanes = tk.Scale(sTray, from_ = 2, to = 10, orient = 'horizontal', length = winH*3/5, resolution = 1)
        self.lanes.grid(column = 0, row = 1, padx = 15, pady = 10)
        
        speedLabel = tk.Label(sTray, text = 'Speed Limit (in MPH):', bg = 'white')
        speedLabel.grid(column = 0, row = 3, sticky = 'w')
        self.speedLim = tk.Scale(sTray, from_ = 25, to = 70, orient = 'horizontal', length = winH*3/5, resolution = 5)
        self.speedLim.grid(column = 0, row = 4, padx = 15, pady = 10)
        
        cpmLabel = tk.Label(sTray, text = 'Cars per Minute:', bg = 'white')
        cpmLabel.grid(column = 0, row = 5, sticky = 'w')
        self.carsPerMin = tk.Scale(sTray, from_ = 5, to = 1000, orient = 'horizontal', length = winH*3/5, resolution = 5)
        self.carsPerMin.grid(column = 0, row = 6, padx = 15, pady = 10)
        
        numSimLabel = tk.Label(sTray, text = 'Number of Simulations:', bg = 'white')
        numSimLabel.grid(column = 0, row = 7, sticky = 'w')
        self.numSim = tk.Scale(sTray, from_ = 10, to = 10000, orient = 'horizontal', length = winH*3/5, resolution = 10)
        self.numSim.grid(column = 0, row = 8, padx = 15, pady = 10)
        
        numSimLabel = tk.Label(sTray, text = 'Simulation Length (in ticks):', bg = 'white')
        numSimLabel.grid(column = 0, row = 9, sticky = 'w')
        self.simLength = tk.Scale(sTray, from_ = 1000, to = 100000, orient = 'horizontal', length = winH*3/5, resolution = 1000)
        self.simLength.grid(column = 0, row = 10, padx = 15, pady = 10)

        #Label for the top tray
        mainLabel = tk.Label(ftTray, text = 'Traffic Simulator', bg = 'white')
        mainLabel.grid(column = 0, row = 0)
        
        # creates check buttons for specific settings for the simulation
        cbDebug = tk.Checkbutton(fbTray, text = 'Enable Debugging', variable = self.boolDebug, command = self.debugWarning)
        cbGraphics = tk.Checkbutton(fbTray, text = 'Enable Graphics', variable = self.boolGraphics, command = self.graphicsCheck)
        cbDebug.grid(column = 3, row = 1, sticky = 'w')
        cbGraphics.grid(column = 3, row = 2, sticky = 'w')
        
        # creates a button tray
        rTray = tk.Frame(content, bg = "grey", height = winH, width = winW/5)
        rTray.grid(column = 4, columnspan = 1, row = 0, rowspan = 8, sticky = ('n', 's', 'e'))
        
        # creates a right side tray
        bTray = tk.Frame(rTray, bg = 'light gray', height = winH*3/8, width = winW/5)
        bTray.grid(column = 0, columnspan = 2, row = 0, rowspan = 4, sticky = 'n')
        
        # Label for the functions
        functLabel = tk.Label(bTray, text = 'Fucntions')
        functLabel.grid(column = 0, row = 0, sticky = ('n', 'w', 'e'))
        
        # buttons to make sim work
        bRun = tk.Button(bTray, text = "Run", command = self.run)
        bUpdate = tk.Button(bTray, text = 'Update', command = self.update)
        bQuit = tk.Button(rTray, text = 'Quit', command = self.quit)
        bRun.grid(column = 0, columnspan = 2,row = 1, padx = 15, pady = 15)
        bUpdate.grid(column = 0, columnspan = 2,row = 2, padx = 15, pady = 10)
        bQuit.grid(column = 0, columnspan = 2,row = 7)
        
        # configures for buttons and labels
        functLabel.config(width = int(winW*4/12/10))
        bRun.config(width = 10)
        bUpdate.config(width = 10)
        bQuit.config(width = 10)
        
        # configs for window itself
        self.window.columnconfigure(0, weight = 1)
        self.window.rowconfigure(0, weight = 1)
        
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
        
        self.window.mainloop()
        return None
        
    # the function for running the simulation
    def run(self):
        # sets the initial values of things
        self.simCancel = False
        self.values = []
        
        # creates a new window for the progress bar and other buttons
        self.progWin = tk.Tk()
        self.progWin.title("SimulationRun")
        
        # creates a style for the progress bar
        style = tk.ttk.Style()
        style.theme_use('default')
        style.configure("black.Horizontal.TProgressbar", background='black')
        
        progLabel = tk.Label(self.progWin, text = 'Simulation Progress:')
        progLabel.grid(column = 0, row = 0, sticky = 'w')
        
        curProgLabel = tk.Label(self.progWin, text= '0.00%')
        curProgLabel.grid(column = 1, row = 0, sticky = 'w')
        
        
        # makes a progress bar set to just under the size of the window
        bar = Progressbar(self.progWin, length = self.window.winfo_screenwidth()/5, style = 'black.Horizontal.TProgressbar')  
        bar.grid(column = 0, columnspan = 4, row = 1, padx = 10, pady = 5)
        
        bCancel = tk.Button(self.progWin, text = 'Cancel', command = self.cancel)
        bCancel.grid(column = 1, row = 2, pady = 5)
        bAnalyse = tk.Button(self.progWin, text = 'Analyse', command = lambda: self.analyse(self.values))
        bAnalyse['state'] = 'disable'
        bAnalyse.grid(column = 0, row = 2, pady = 5)

        self.progWin.update()

        simiters = 0.0
        for i in range(self.numSim.get()):
            sim = s.simulator( self.lanes.get(), 6, self.boolDebug.get(), self.speedLim.get(), self.boolGraphics.get(), self.simLength.get(), self.simLength.get()-200, 1)

            sim.start()
            self.values.append(sim.RESULTS)
            simiters += 1.0
            bar['value'] = simiters / float(self.numSim.get()) * 100.0
            curProgLabel['text'] = str(bar['value']) + "%"
            self.progWin.update()
            if(self.simCancel):
                self.progWin.destroy()
                messagebox.showwarning('Sim Canceled', 'Simulation has been interrupted.')
                return


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
            
        print(self.numSim.get())
            
    def debugWarning(self):
        if(not self.boolDebug.get()):
            messagebox.showwarning('Debugging Enabled','Debugging will slow down the simulation\n speed and may cause the system to crash.')
            self.boolDebug.set(True)
        else:
            self.boolDebug.set(False)
            
    def cancel(self):
        self.simCancel = messagebox.askyesno('Cancel Sim','Do you want to cancel the sim?')
        
    def analyse(self, values):
        self.progWin.destroy()
        print(values)
        
    def update(self):
        messagebox.showwarning('Update Sim', 'Simulation has been updated.')
        
    def quit(self):
        quit = messagebox.askokcancel('Quit','Quitting simulation.')
        if(quit):
            self.window.destroy()
            self.window.quit()
        else: return
        
        
app = StartUI()
