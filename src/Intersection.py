import math
from src.Surface import Surface
from collections import defaultdict


class Intersection(Surface):

    lane_width = 10

    def __init__(self, center, radius, speed_limit):
        """
        :param anchor_corner: [double, double]
        :param length: double
        :param inbound_lanes: int
        :param outbound_lanes: int
        :param orientatino: double (IN RADIANS!)
        :param speed_limit: int
        """
        self.center = center
        self.radius = radius
        self.speed_limit = speed_limit
        self.vehicles = []
        # These lists are all same-indexed
        # Roads are ordered by orientation
        self.adjacent_roads = []
        self.adjacent_road_orientations = []
        self.adjacent_road_widths = []
        # List of tuples storing the bounds on the angle centered at the origin subtended by the road
        self.adjacent_road_bounding_orientations = []
        self.next_locations = [] # Prevents conflicts with cars being moved between tick and tock.

    def tick(self, ticktime_ms):
        """
        Performs the vehicle next location getting tick
        :param ticktime_ms:
        :return:
        """

        self.next_locations = self.request_next_locations(ticktime_ms)

        return

    def tock_positions(self):
        """
        Performs the vehicle position updating tock
        :return:
        """

        self.update_positions()

        return

    def tock_crashes(self):
        """
        Performs the crash detecting and handling tock
        :return:
        """

        self.process_collisions()

        return

    def request_next_locations(self, ticktime_ms):
        """
        Produces the next intended location of each car.
        :param ticktime_ms:
        :return:
        """
        next_locations = [[vehicle.compute_next_location(ticktime_ms), vehicle] for vehicle in self.vehicles]
        return next_locations

    def is_local_in_intersection(self, location):
        """
        Takes a local coordinate and returns whether or not it is in the intersection
        :param location:
        :return:
        """
        # Checking if something is in a circle centered at the origin is so pleasant
        result = (math.sqrt(math.pow(location[0], 2) + math.pow(location[1], 2)) < self.radius)
        return result

    def is_global_in_intersection(self, location):
        """
        Takes a global coordinate and returns whether or not it is in the intersection
        :param location:
        :return:
        """
        recast = [location[0] - self.center[0], location[1] - self.center[1]]
        result = (math.sqrt(math.pow(recast[0], 2) + math.pow(recast[1], 2)) < self.radius)
        return result

    def local_to_global_location_conversion(self, location):
        """
        Turn a local coordinate into its corresponding global coordinate
        :param location:
        :return:
        """
        return [location[0] + self.center[0], location[1] + self.center[1]]

    def global_to_local_location_conversion(self, location):
        """
        Turn a global coordinate into its corresponding local coordinate
        :param location:
        :return:
        """
        return [location[0] - self.center[0], location[1] - self.center[1]]

    # I love circles so much. They are my best friends. -P

    def which_neighbor(self, location):
        """
        Takes a global coordinate and returns which, if any of the neighboring roads contains that coordinate
        :param location:
        :return:
        """

        for road in self.adjacent_roads:
            if road.is_global_on_road(location):
                return road
        raise ValueError("No neighbor contains that location.")

    def transfer(self, vehicle, location):
        """
        Takes a vehicle and a global location and attempts to relocate the vehicle to that location
        :param vehicle:
        :param location:
        :return:
        """

        try:
            neighbor = self.which_neighbor(location)
            neighbor.accept_transfer(vehicle, location)
            self.vehicles.remove(vehicle)
        except ValueError:
            raise ValueError("A vehicle couldn't be transferred because it requested an invalid destination.")

        return

    def accept_transfer(self, vehicle, location):
        """
        Takes a vehicle and a global coordinate and places the vehicle at the local version of the coordinate.
        :param vehicle:
        :param location:
        :return:
        """

        self.vehicles.append(vehicle)
        local_location = self.global_to_local_location_conversion(location)
        vehicle.transfer_to_intersection(self, local_location)

        return

    def update_positions(self):
        """
        Updates the position of each vehicle on the intersection.
        :return:
        """
        # Update the location of each vehicle by updating it directly or transferring it to a neighboring road
        for intended_location, vehicle in self.next_locations:
            if self.is_local_in_intersection(intended_location):
                vehicle.update_location(intended_location[0], intended_location[1])
            else:
                global_location = self.local_to_global_location_conversion(intended_location)
                self.transfer(vehicle, global_location)

        # Reset the list of cars intending to move
        self.next_locations = []

        return

    def process_collisions(self):
        """
        Discovers which vehicles have crashed and informs them.
        :return:
        """

        return

    def spawn(self, vehicle_template, driver_template, direction):
        """
        Takes the necessary inputs to generate a vehicle and generates the corresponding vehicles at a
        random location in the intersection
        :param vehicle_template:
        :param driver_template:
        :param direction:
        :return:
        """
        return

    def add_neighboring_road(self, road):
        """
        Takes a road and adds it to the intersection.
        This is assumed to be unable to fail, as non-physical roads should have errored before the simulation.
        :param road:
        :return:
        """

        orientation = road.orientation
        width = road.width
        sine = (width / 2) / self.radius
        angle = math.asin(sine)
        upper_angle = (orientation + angle) % (2 * math.pi)
        lower_angle = (orientation - angle) % (2 * math.pi)
        # Now insert all of this information at the correct location
        if len(self.adjacent_roads) == 0:
            self.adjacent_roads.append(road)
            self.adjacent_road_orientations.append(orientation)
            self.adjacent_road_widths.append(width)
            self.adjacent_road_bounding_orientations.append((upper_angle, lower_angle))
        elif len(self.adjacent_roads) == 1:
            # should never be equal
            if self.adjacent_road_orientations[0] < orientation:
                index = 1
            else:
                index = 0
            self.adjacent_roads.insert(index, road)
            self.adjacent_road_orientations.insert(index, orientation)
            self.adjacent_road_widths.insert(index, width)
            self.adjacent_road_bounding_orientations.insert(index, (upper_angle, lower_angle))
        else:
            # It's like adding a spoke at the right place in a wheel
            for i in range(len(self.adjacent_roads)):
                if (self.adjacent_road_orientations[i] < orientation) and (self.adjacent_road_orientations[i + 1] > orientation):
                    index = i + 1
                    self.adjacent_roads.insert(index, road)
                    self.adjacent_road_orientations.insert(index, orientation)
                    self.adjacent_road_widths.insert(index, width)
                    self.adjacent_road_bounding_orientations.insert(index, (upper_angle, lower_angle))
                    break

        return