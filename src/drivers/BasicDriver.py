class BasicDriver:

    def __init__(self):
        # over_breaking defines by what percentage driver will over compensate in breaking
        # as a function of time until collision
        self.over_breaking = .1

        # comfortable following time
        self.following_time = 3

        # max braking decel of car
        self.max_break_decel = 4.5

        # max acceleration of vehicle
        self.max_accel = 2

        # time to achieve speed limit on the road from current velocity
        self.accel_time = 10

        # time interval to update neighbors
        self.update_time_ms = 30