import time
import operator
from src.vehicles.VehicleTemplate import VehicleTemplate
from src.drivers.DriverTemplate import DriverTemplate
import math


class Vehicle:

    class VehicleNeighbors:

        def __init__(self):
            self.last_update_time_ms = 0
            self.nearby_vehicles = []
            self.vehicles_behind = []
            self.vehicles_infront = []

    def __init__(self, road, x=0, y=0, vx=0, vy=0, orientation=0, cartype=VehicleTemplate(), drivertype=DriverTemplate()):
        """
        :param road: Road
        :param ticktime_ms: float
        ticktime_ms is the time between simulation ticks in ms
        :param x: float
        :param y: float
        :param vx: float
        :param vy: float
        :param orientation: double
        :param cartype:
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = 0
        self.ay = 0
        self.orientation = orientation
        self.road = road
        self.intersection = None
        self.vehicle_neigbors = self.VehicleNeighbors()
        self.cartype = cartype
        self.drivertype = drivertype
        self.bucket = None

    def set_bucket(self, bucket):
        """
        Sets the bucket in which the car resides
        :param bucket:
        :return:
        """
        self.bucket = bucket
        return

    def get_bucket(self):
        """
        Gets the bucket in which the car resides
        :return:
        """
        return self.bucket

    def get_location(self):
        """
        Returns the vehicle's current local location
        :return:
        """
        return (self.x, self.y)

    def get_bounding_points(self):
        """
        Computes and returns the four points on the corners of the vehicle.
        Used for collision detection.
        :return:
        """

        location = (self.x, self.y)
        # Compute the points at the origin with orientation 0, then rotate by orientation, then shift by location
        p1 = tuple(map(operator.add, location, self.rotate_around_origin(-self.cartype.length / 2, -self.cartype.width / 2,
                                                  self.orientation)))
        p2 = tuple(map(operator.add, location, self.rotate_around_origin(self.cartype.length / 2, -self.cartype.width / 2,
                                                  self.orientation)))
        p3 = tuple(map(operator.add, location, self.rotate_around_origin(self.cartype.length / 2, self.cartype.width / 2,
                                                  self.orientation)))
        p4 = tuple(map(operator.add, location, self.rotate_around_origin(-self.cartype.length / 2, self.cartype.width / 2,
                                                  self.orientation)))

        return (p1, p2, p3, p4)

    def max_offset(self):
        """
        The largest distance of any point on the vehicle from the location of the vehicle.
        Used to shortcut collision detection.
        :return:
        """

        return math.sqrt(math.pow(self.cartype.width / 2, 2) + math.pow(self.cartype.length / 2, 2))

    def rotate_around_origin(self, x, y, radians):

        rot_x = x * math.cos(radians) - y * math.sin(radians)
        rot_y = y * math.cos(radians) + x * math.sin(radians)

        return (rot_x, rot_y)

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

        time_untilx = abs(self.x - vehicle.x) / abs(vehicle.vx - self.vx)

        time_untily = time_untilx
        if vehicle.vy != self.vy:
            time_untily = abs(self.y - vehicle.y) / abs(vehicle.vy - self.vy)

        if time_untilx > 0 and time_untily > 0 and abs(time_untilx - time_untily) < 2:
            return min(time_untilx, time_untily)

        return -1

    def compute_next_location(self, ticktime_ms):
        """
        called by the road to update the cars intended positions
        TODO: update method to allow smooth acceleration in traffic
        :return: (float, float)
        """
        brake_decel = 0


        for vehicle in self.vehicle_neigbors.nearby_vehicles:
            brake_decel += self.respond_vehicle_brake(vehicle)

        for vehicle in self.vehicle_neigbors.vehicles_infront:
            brake_decel += self.respond_vehicle_brake(vehicle)

        for vehicle in self.vehicle_neigbors.vehicles_behind:
            brake_decel += self.respond_vehicle_brake(vehicle)

        brake_decel = min(brake_decel, self.cartype.max_brake_decel)

        if brake_decel > 0:
            self.ax = -brake_decel
        else:
            if self.road.speed_limit + self.drivertype.speeding_offset > self.vx:
                self.ax = min((self.road.speed_limit - self.vx) / self.drivertype.accel_time, self.drivertype.max_accel)

        self.vx += self.ax * ticktime_ms / 1000

        self.vy += self.ay * ticktime_ms / 1000

        return self.x + self.vx * ticktime_ms / 1000, self.y + self.vy * ticktime_ms / 1000

    def update_vehicle_neighbors(self, nearby_vehicles, vehicles_behind, vehicles_infront):
        """
        :param nearby_vehicles: Vehicle list
        must have the car in front inside this list to properly respond
        called from Road
        :return: None
        """
        if self.vehicle_neigbors.last_update_time_ms < int(time.time() * 1000):
            self.vehicle_neigbors.nearby_vehicles = nearby_vehicles
            self.vehicle_neigbors.vehicles_behind = vehicles_behind
            self.vehicle_neigbors.vehicles_infront = vehicles_infront
            self.vehicle_neigbors.last_update_time_ms = int(time.time() * 1000)

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
        timeuntil = self.get_time_until_collision(other_vehicle)
        if timeuntil <= self.drivertype.following_time and timeuntil > 0:
            return min((self.vx - other_vehicle.vx) / timeuntil, self.cartype.max_brake_decel)

        else:
            return 0
