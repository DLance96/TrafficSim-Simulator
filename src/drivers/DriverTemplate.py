class DriverTemplate:

    def __init__(self):
        # over_breaking defines by what percentage driver will over compensate in breaking
        # as a function of time until collision
        self.over_braking_factor = .1

        # comfortable following time
        self.following_time = 3

        # max acceleration of driver
        self.max_accel = 2

        # minimum acceleration of driver
        self.min_accel = 0

        # maximum speed driver is willing to go
        self.max_speed = 200

        # time to achieve speed limit on the road or desired speed from current velocity
        self.accel_time = 10

        # time interval to update neighbors
        self.update_time_ms = 30