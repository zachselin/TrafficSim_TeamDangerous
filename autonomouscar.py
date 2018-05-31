from car import Car
import shared as g

class Autonomous(Car):

    def __init__(self, sim, lane, speed, maxspeed, id, carAhead, carUpAhead, carDownAhead, laneidx, size, canvasheight,
                 lanes):
        super(Autonomous, self).__init__(sim, lane, speed, maxspeed, id, carAhead, carUpAhead, carDownAhead, laneidx, size,
                                         canvasheight, lanes)
        self.color = g.autonomouscolor
        self.name = "autonomous"

    def general_behavior(self):
        # AUTONOMOUS VEHICLE BEHAVIOR HERE

        # TEMPORARY - IMPLEMENTS SAME AS PARENT BEHAVIOR
        super(Autonomous, self).general_behavior()