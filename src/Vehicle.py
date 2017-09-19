
class Vehicle:

    def __init__(self, template=None):
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.orientation = 0

        if template is None:
            self.length = 4
            self.width = 2
