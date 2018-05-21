class Car:
    def __init__(self, lane, speed):
        self.shape = canvas.create_rectangle(0, 7+(HEIGHT/2) + ( (lane - 3) *30), SIZE/2, 7+SIZE/4+(HEIGHT/2) + ( (lane - 3) *30), fill=color)
        self.speedx = speed
        self.speedy = 0
        self.active = True
        self.move_active()


    def car_update(self):
        canvas.move(self.shape, self.speedx, self.speedy)
       
    def move_active(self):
        if self.active:
            self.ball_update()
            tk.after(40, self.move_active) # changed from 10ms to 30ms
       
    def emergencyDeccel(self):
        print()
            
    def hardDeccel(self):
        print()
        
    def easyDeccel(self):
        print()
    
    def laneChange(self):
        print()
    
    def easyAccel(self):
        print()
        
    def hardAccel(self):
        print()
