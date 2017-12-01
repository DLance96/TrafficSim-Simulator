from pygame.locals import *


class DriverTemplate:

    def __init__(self):
        # over_breaking defines by what percentage driver will over compensate in breaking
        # as a function of time until collision
        self.over_braking_factor = .1

        # speed to drive over speed limit
        self.speeding_offset = 0

        # comfortable following time
        self.following_time = 3

        # max acceleration of driver
        self.max_accel = 4

        # minimum acceleration of driver
        self.min_accel = 0

        # maximum speed driver is willing to go
        self.max_speed = 200

        # time to achieve speed limit on the road or desired speed from current velocity
        self.accel_time = 10

        # time interval to update neighbors
        self.update_time_ms = 30

        self.intersection_prep_time = 6

        self.color = Color(255, 100, 100)


class SlowDriver(DriverTemplate):

    def __init__(self):
        DriverTemplate.__init__(self)
        self.max_speed = 100
        self.max_accel = 1.4
        self.color = Color(100, 255, 255)


class SpeedoFerraro(DriverTemplate):

    def __init__(self):
        DriverTemplate.__init__(self)
        self.max_accel = 100
        self.min_accel = 10
        self.max_speed = 2000
        self.accel_time = 1
        self.following_time = 1
        self.speeding_offset = 100
        self.color = Color(100, 100, 255)
