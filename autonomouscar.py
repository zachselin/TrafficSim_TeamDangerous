from car import Car

class Autonomous(Car):

    def __init__(self, lane, speed, maxspeed, id, carAhead, carUpAhead, carDownAhead, laneidx, size, canvasheight,
                 lanes):
        super(Autonomous, self).__init__(lane, speed, maxspeed, id, carAhead, carUpAhead, carDownAhead, laneidx, size,
                                         canvasheight, lanes)

    def general_behavior(self):
        # AUTONOMOUS VEHICLE BEHAVIOR HERE

        # TEMPORARY - IMPLEMENTS SAME AS PARENT BEHAVIOR
        super(Autonomous, self).general_behavior()