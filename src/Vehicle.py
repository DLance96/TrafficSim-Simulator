import time

class Vehicle:

    def __init__(self, road, ticktime_ms, x = 0, y = 0, vx = 0, vy = 0, orientation = 0):
        """
        :param road: Road
        :param ticktime: float
        ticktime is the time between simulation ticks in ms
        :param x: float
        :param y: float
        :param vx: float
        :param vy: float
        :param orientation: int
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = 0
        self.ay = 0
        self.orientation = orientation
        self.ticktime_ms = ticktime_ms
        self.road = road
        self.init_vehicle_size()
        self.init_vehicle_behavior()
        self.vehicle_neigbors = Vehicle_Neighbors()

    def init_vehicle_behavior(self):
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

    def init_vehicle_size(self):
        self.length = 4
        self.width = 2


    def get_intended_position(self, time_ahead):
        """
        :param time_ahead: float
        time_ahead is how many seconds in the future this predicted position
        occurs
        :return: tuple
        """
        return self.x + self.vx * time_ahead, self.y + self.vy * time_ahead

    def get_time_until_collision(self, vehicle):
        if vehicle.vx == self.vx:
            return -1
        if vehicle.vy == self.vy:
            return -1

        time_untilx = (self.x - vehicle.x) / (vehicle.vx - self.vx)

        time_untily = (self.y - vehicle.y) / (vehicle.vy - self.vy)

        if time_untilx > 0 and time_untily > 0 and abs(time_untilx - time_untily) < 2:
            return min(time_untilx, time_untily)

        return -1

    def update_self(self):
        """
        called by the road to update the cars intended positions
        TODO: update method to allow smooth acceleration in traffic
        :return:
        """
        brake_decel = 0
        for vehicle in self.vehicle_neigbors.nearby_vehicles:
            brake_decel += self.respond_vehicle_brake(vehicle)

        brake_decel = min(brake_decel, self.max_break_decel)

        if brake_decel > 0:
            self.ax = -brake_decel
        else:
            if self.road.speed_limit > self.vx:
                self.ax = min((self.road.speed_limit - self.vx) / self.accel_time, self.max_accel)





    def tick(self):
        """
        called after all cars have run update_self
        is only called by the road
        :return: None
        """
        self.vx += self.ax * self.ticktime_ms / 1000

        self.vy += self.ay * self.ticktime_ms / 1000

        self.x += self.vx * self.ticktime_ms / 1000

        self.y += self.vy * self.ticktime_ms / 1000

    def respond_vehicle_brake(self, other_vehicle):
        """
        calculates proper braking force required to not crash
        :param other_vehicle: Vehicle
        :return: tuple
        returns float
        deceleration along x
        """
        if self.vx > other_vehicle.vx and self.x <= other_vehicle.x:
            timeuntil = self.get_time_until_collision(other_vehicle)
            if timeuntil <= self.following_time:
                return min((self.vx - other_vehicle.vx) / timeuntil, self.max_break_decel)


        else:
            return 0



class Vehicle_Neighbors:

    def __init__(self):
        self.last_update_time = 0
        self.nearby_vehicles = []

    def update(self, nearby_vehicles):
        """
        :param nearby_vehicles: Vehicle list
        must have the car in front inside this list to properly respond
        update only when last_update_time < current_time - car's update_ime
        :return: None
        """
        self.nearby_vehicles = nearby_vehicles
        self.last_update_time = int(time.time() * 1000)