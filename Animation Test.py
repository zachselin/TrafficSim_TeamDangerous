from tkinter import *
import time
import numpy as np

WIDTH = 2000
HEIGHT = 300
SIZE = 60
tk = Tk()
canvas = Canvas(tk, width=WIDTH, height=HEIGHT, bg="green")
canvas.pack()
canvas.create_line(0,(HEIGHT/2), WIDTH,(HEIGHT/2), width="120", fill="grey")
canvas.create_line(0,(HEIGHT/2)+60, WIDTH,(HEIGHT/2)+60, width="3", fill="white")
canvas.create_line(0,(HEIGHT/2)-60, WIDTH,(HEIGHT/2)-60, width="3", fill="white")
canvas.create_line(0,(HEIGHT/2)+30, WIDTH,(HEIGHT/2)+30, width="1", fill="white")
canvas.create_line(0,(HEIGHT/2)-30, WIDTH,(HEIGHT/2)-30, width="1", fill="white")
canvas.create_line(0,(HEIGHT/2), WIDTH,(HEIGHT/2), width="1", fill="white")
color = 'red'
class Car:
    def __init__(self, lane, speed):
        self.shape = canvas.create_rectangle(0 - 25, 7+(HEIGHT/2) + ( (lane - 3) *30), SIZE/2 - 25, 7+SIZE/4+(HEIGHT/2) + ( (lane - 3) *30), fill=color)
        self.speedx = speed
        self.speedy = 0 
        self.count = 0
        self.speed = True
        self.active = True
        self.move_active()

    def decelerate(self):
        self.speedx *= .90
        print(self.speedx)
        if (self.speedx < 0.5):
            self.speed = False

    def accelerate(self):
        self.speedx *= 1.10
        print(self.speedx)
        if (self.speedx > 2.0):
            self.speed = True

    def ball_update(self):
        canvas.move(self.shape, self.speedx, self.speedy)
        if (self.count == 50):
            if (self.speed):
                self.decelerate()
            else:
                self.accelerate()
            self.count = 0
        else:
            self.count = self.count + 1

    def move_active(self):
        if self.active:
            self.ball_update()
            tk.after(10, self.move_active) # changed from 10ms to 30ms

def make_car():
        lane = np.random.randint(1,5)
        speed = np.random.uniform(.5,1)
        car = Car(lane, speed)
        tk.after(1000, make_car)    
make_car()




tk.mainloop()