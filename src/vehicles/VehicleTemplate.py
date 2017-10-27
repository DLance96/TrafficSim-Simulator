from pygame.locals import *
class VehicleTemplate:
    def __init__(self):

        # length of vehicle
        self.length = 8

        # width of vehicle

        self.width = 4

        # max braking decel of car
        self.max_brake_decel = 4.5

        # max acceleration of vehicle
        self.max_accel = 2

        # mass of vehicle
        self.mass = 2000

        # maximum speed of vehicle
        self.max_speed = 200

        self.color = Color(255, 100, 100)

class Ferrari(VehicleTemplate):

    def __init__(self):
        VehicleTemplate.__init__()
        self.max_accel = 6
        self.max_speed = 400