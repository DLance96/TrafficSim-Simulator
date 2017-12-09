from pygame.locals import *


class DriverTemplate:
    """
    Provides a collection of information needed by a vehicle to determine driving behavior.
    The information stored in a DriverTemplate is relevant to the properties of the driver.
    """

    def __init__(self, over_braking_factor = 0.1, speeding_offset = 0,
                 following_time = 3, max_accel = 6,
                 min_accel = 0, max_speed = 200,
                 accel_time = 10, update_time_ms = 30,
                 intersection_prep_time = 6,
                 color = Color(255, 100, 100)):
        # over_breaking defines by what percentage driver will over compensate in breaking
        # as a function of time until collision
        self.over_braking_factor = over_braking_factor

        # speed to drive over speed limit
        self.speeding_offset = speeding_offset

        # comfortable following time
        self.following_time = following_time

        # max acceleration of driver
        self.max_accel = max_accel

        # minimum acceleration of driver
        self.min_accel = min_accel

        # maximum speed driver is willing to go
        self.max_speed = max_speed

        # time to achieve speed limit on the road or desired speed from current velocity
        self.accel_time = accel_time

        # time interval to update neighbors
        self.update_time_ms = update_time_ms

        self.intersection_prep_time = intersection_prep_time

        self.color = color
