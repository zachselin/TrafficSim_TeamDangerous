from car import Car
import shared as g

class BufferBuilder(Car):

    def __init__(self, sim, lane, speed, maxspeed, id, carAhead, carUpAhead, carDownAhead, laneidx, size, canvasheight,
                 lanes):
        super(BufferBuilder, self).__init__(sim, lane, speed, maxspeed, id, carAhead, carUpAhead, carDownAhead, laneidx, size,
                                         canvasheight, lanes)
        self.color = g.buffercolor

    def general_behavior(self):
        # AUTONOMOUS VEHICLE BEHAVIOR HERE

        # TEMPORARY - IMPLEMENTS SAME AS PARENT BEHAVIOR
        super(BufferBuilder, self).general_behavior()
