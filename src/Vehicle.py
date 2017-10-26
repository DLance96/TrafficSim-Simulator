import time

from vehicles.VehicleTemplate import StandardCar
from drivers.DriverTemplate import BasicDriver


class Vehicle:

    class VehicleNeighbors:

        def __init__(self):
            self.last_update_time_ms = 0
            self.nearby_vehicles = []

    def __init__(self, road, ticktime_ms, x=0, y=0, vx=0, vy=0, orientation=0, cartype=StandardCar(), drivertype=BasicDriver()):
        """
        :param road: Road
        :param ticktime_ms: float
        ticktime_ms is the time between simulation ticks in ms
        :param x: float
        :param y: float
        :param vx: float
        :param vy: float
        :param orientation: int
        :param cartype:
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
        self.intersection = None
        self.vehicle_neigbors = self.VehicleNeighbors()
        self.cartype = cartype
        self.drivertype = drivertype


    def get_intended_position(self, time_ahead):
        """
        :param time_ahead: float
        time_ahead is how many seconds in the future this predicted position
        occurs
        :return: tuple
        """
        return self.x + self.vx * time_ahead, self.y + self.vy * time_ahead

    # Takes a road and a local location and sets the car to being on that road at that location
    def transfer_to_road(self, road, location):
        self.road = road
        self.intersection = None
        self.x = location[0]
        self.y = location[1]
        return

    # Takes an intersection and a local location and sets the car to being in that intersection at that location
    def transfer_to_intersection(self, intersection, location):
        self.road = None
        self.intersection = intersection
        self.x = location[0]
        self.y = location[1]
        return

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

    def compute_next_location(self):
        """
        called by the road to update the cars intended positions
        TODO: update method to allow smooth acceleration in traffic
        :return: (float, float)
        """
        brake_decel = 0
        for vehicle in self.vehicle_neigbors.nearby_vehicles:
            brake_decel += self.respond_vehicle_brake(vehicle)

        brake_decel = min(brake_decel, self.drivertype.max_brake_decel)

        if brake_decel > 0:
            self.ax = -brake_decel
        else:
            if self.road.speed_limit > self.vx:
                self.ax = min((self.road.speed_limit - self.vx) / self.drivertype.accel_time, self.drivertype.max_accel)

        self.vx += self.ax * self.ticktime_ms / 1000

        self.vy += self.ay * self.ticktime_ms / 1000

        return (self.x + self.vx * self.ticktime_ms / 1000, self.y + self.vy * self.ticktime_ms / 1000)

    def update_vehicle_neighbors(self, nearby_vehicles):
        """
        :param nearby_vehicles: Vehicle list
        must have the car in front inside this list to properly respond
        called from Road
        :return: None
        """
        if nearby_vehicles.last_update_time_ms < int(time.time() * 1000):
            self.nearby_vehicles.nearby_vehicles = nearby_vehicles
            self.nearby_vehicles.last_update_time_ms = int(time.time() * 1000)

    def update_location(self, x, y):
        """
        called after all cars have run update_self
        is only called by the road
        :return: None
        """
        self.x = x

        self.y = y

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
            if timeuntil <= self.drivertype.following_time:
                return min((self.vx - other_vehicle.vx) / timeuntil, self.drivertype.max_break_decel)


        else:
            return 0
