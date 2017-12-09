from pygame.locals import *


class VehicleTemplate:
    """
    Provides a collection of information needed by a vehicle to determine driving behavior.
    The information stored in a DriverTemplate is relevant to the properties of the vehicle
    """


    def __init__(self, length = 8, width = 4,
                 max_decel = 9, max_accel = 6,
                 mass = 2000, max_speed = 200,
                 max_turn_rad_per_sec = 3, color = Color(255, 100, 100)):

        # length of vehicle
        self.length = length

        # width of vehicle
        self.width = width

        # max braking decel of car
        self.max_brake_decel = max_decel

        # max acceleration of vehicle
        self.max_accel = max_accel

        # mass of vehicle
        self.mass = mass

        # maximum speed of vehicle
        self.max_speed = max_speed

        self.max_turn_rad_per_sec = max_turn_rad_per_sec

        self.color = color

# For reference
"""
class Ferrari(VehicleTemplate):

    def __init__(self):
        VehicleTemplate.__init__(self)
        self.max_accel = 11
        self.max_speed = 200
        self.color = Color(10, 231, 255)
"""
