import time
import operator
import random
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

    def __init__(self, road, x=0, y=0, vx=0, vy=0, orientation=0, cartype=VehicleTemplate(),
                 drivertype=DriverTemplate()):
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
        self.last_road = None
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
        p1 = tuple(
            map(operator.add, location, self.rotate_around_origin(-self.cartype.length / 2, -self.cartype.width / 2,
                                                                  self.orientation)))
        p2 = tuple(
            map(operator.add, location, self.rotate_around_origin(self.cartype.length / 2, -self.cartype.width / 2,
                                                                  self.orientation)))
        p3 = tuple(
            map(operator.add, location, self.rotate_around_origin(self.cartype.length / 2, self.cartype.width / 2,
                                                                  self.orientation)))
        p4 = tuple(
            map(operator.add, location, self.rotate_around_origin(-self.cartype.length / 2, self.cartype.width / 2,
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

    def predict_target_position(self, time_ahead):
        """
        :param time_ahead: float
        time_ahead is how many seconds in the future this predicted position
        occurs
        :return: tuple
        """
        return self.x + self.vx * time_ahead, self.y + self.vy * time_ahead

    def correct_direction(self):
        return -1 if (self.y <= self.road.lane_width * self.road.outbound_lanes) else 1

    # Takes a road and a local location and sets the car to being on that road at that location
    # Cars enter roads parallel to the road
    def transfer_to_road(self, road, location):
        self.road = road
        self.intersection = None
        self.x = location[0]
        self.y = location[1]
        orientation = road.orientation
        new_velocity = self.rotate_around_origin(self.vx, self.vy, -orientation)
        self.orientation = 0
        self.vx = new_velocity[0]
        self.vy = new_velocity[1]
        return

    # Takes an intersection and a local location and sets the car to being in that intersection at that location
    def transfer_to_intersection(self, intersection, location, orientation):
        self.road = None
        self.intersection = intersection
        self.x = location[0]
        self.y = location[1]
        # Major simplifying assumption, cars enter intersections parallel to the road they were on
        # vehicle_orientation = vehicle.orientation
        new_velocity = self.rotate_around_origin(self.vx, self.vy, orientation)
        self.orientation = orientation
        self.vx = new_velocity[0]
        self.vy = new_velocity[1]
        return

    def time_until_collision_road(self, vehicle):
        if abs(vehicle.y - self.y) * 2 > self.cartype.width + vehicle.cartype.width:
            return -1
        if vehicle.vx == self.vx:
            return -1

        time_untilx = (self.x - vehicle.x) / (vehicle.vx - self.vx)

        return time_untilx

    def time_until_collision(self, vehicle):
        if self.road is not None:
            return self.time_until_collision_road(vehicle)
        return 0

    def compute_following_time_road(self, vehicle):
        direction = self.correct_direction()
        if abs(vehicle.y - self.y) * 2 > self.cartype.width + vehicle.cartype.width:
            return -1
        if 0 == self.vx:
            return -1
        if self.vx * direction <= vehicle.vx * direction:
            return -1;
        following_time = (abs(vehicle.x - self.x) - vehicle.cartype.length) / abs(self.vx)

        return following_time

    def compute_following_time(self, vehicle):
        if self.road is not None:
            return self.compute_following_time_road(vehicle)
        return 0

    def compute_next_location_road(self, ticktime_ms):
        """
               called by the road to update the cars intended positions
               TODO: update method to allow smooth acceleration in traffic
               :return: (float, float)
               """
        brake_decel = 0
        slowdown_decel = 0
        direction = self.correct_direction()

        # compute desired braking and slowdown
        for vehicle in self.vehicle_neigbors.nearby_vehicles:
            brake_decel += self.respond_vehicle_brake(vehicle)
            slowdown_decel += self.respond_vehicle_slowdown(vehicle)

        for vehicle in self.vehicle_neigbors.vehicles_infront:
            brake_decel += self.respond_vehicle_brake(vehicle)
            slowdown_decel += self.respond_vehicle_slowdown(vehicle)

        for vehicle in self.vehicle_neigbors.vehicles_behind:
            brake_decel += self.respond_vehicle_brake(vehicle)
            slowdown_decel += self.respond_vehicle_slowdown(vehicle)

        brake_decel = min(brake_decel, self.cartype.max_brake_decel)

        # if need to brake
        if brake_decel > 0:
            # prevents braking from becoming reversing
            if abs(brake_decel * ticktime_ms / 1000) < abs(self.vx):
                self.ax = -brake_decel * direction
            else:
                self.ax = -self.vx / (ticktime_ms / 1000)
        else:
            # compute acceleration as sum of desired accel and slowdown
            if self.road.speed_limit + self.drivertype.speeding_offset > abs(self.vx):
                self.ax = direction * min((self.road.speed_limit - abs(self.vx)) / self.drivertype.accel_time,
                                          self.drivertype.max_accel)
                # make sure slowdown does not cause braking
                self.ax += -slowdown_decel * direction

        # increment vx by ax
        self.vx += self.ax * ticktime_ms / 1000
        # increment vy by ay
        self.vy += self.ay * ticktime_ms / 1000

        # return next position based on vx, vy
        return self.x + self.vx * ticktime_ms / 1000, self.y + self.vy * ticktime_ms / 1000

    def compute_next_location_intersection(self, ticktime_ms):
        """
        :param ticktime_ms:
        :return:
        """
        roadno = random.randint(0, len(self.intersection.adjacent_road_bounding_orientations)-1)
        # roadno = 1
        orientation = self.intersection.adjacent_road_bounding_orientations[roadno][0] - math.pi/10
        globalx, globaly = self.intersection.local_to_global_location_conversion((self.x, self.y))
        destination = (self.intersection.center[0] + math.cos(orientation) * self.intersection.radius*1.1,
                       self.intersection.center[1] + math.sin(orientation) * self.intersection.radius*1.1)
        accel_vector = (destination[0] - globalx, destination[1] - globaly)
        # self.ax = accel_vector[0]*2
        # self.ay = accel_vector[1]*2

        # self.vx += self.ax * ticktime_ms / 1000
        # self.vy += self.ay * ticktime_ms / 1000
        self.vx = accel_vector[0]/10
        self.vy = accel_vector[1]/10
        return self.x + self.vx * ticktime_ms / 1000, self.y + self.vy * ticktime_ms / 1000

    def compute_next_location(self, ticktime_ms):

        if self.road is not None:
            behind = []
            infront = []
            if self.bucket.get_previous_alive_bucket() is not None:
                behind = self.bucket.get_previous_alive_bucket().vehicles
            if self.bucket.get_next_alive_bucket() is not None:
                infront = self.bucket.get_next_alive_bucket().vehicles
            self.update_vehicle_neighbors(self.bucket.vehicles, behind, infront)

            return self.compute_next_location_road(ticktime_ms)
        elif self.intersection is not None:
            return self.compute_next_location_intersection(ticktime_ms)

        return self.x, self.y

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

    def respond_vehicle_slowdown(self, other_vehicle):
        """
        calculates slowdown required not to crash
        :param other_vehicle:
        :return: float
        """
        timeuntil = self.compute_following_time(other_vehicle)
        direction = self.correct_direction()

        if 0 <= timeuntil:
            if self.x * direction < other_vehicle.x * direction:
                return (self.drivertype.following_time / timeuntil) * abs(self.vx - other_vehicle.vx) / timeuntil

        return 0

    def respond_vehicle_brake(self, other_vehicle):
        """
        calculates proper braking force required to not crash
        :param other_vehicle: Vehicle
        :return: float
        returns float
        deceleration along x
        """
        timeuntil = self.compute_following_time(other_vehicle)
        direction = self.correct_direction()

        if 0 <= timeuntil <= self.drivertype.following_time:
            if self.x * direction < other_vehicle.x * direction:
                return min(
                    (1 + self.drivertype.over_braking_factor * self.drivertype.following_time / timeuntil) * abs(
                        self.vx - other_vehicle.vx) / timeuntil, self.cartype.max_brake_decel)
            else:
                return 0

        else:
            return 0

    def collided(self, other_vehicle):
        """
        Processes a vehicle having collided with another vehicle
        :param other_vehicle:
        :return:
        """
        # print("A collision has occured!")
        return
