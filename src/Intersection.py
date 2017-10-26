import math
from collections import defaultdict


class Intersection:

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
        self.adjacent_roads = []
        self.adjacent_road_orientations = []
        self.adjacent_road_widths = []
        self.next_locations = [] # Prevents conflicts with cars being moved onto roads between tick and tock.

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
        next_locations = [[vehicle.get_intended_position(ticktime_ms), vehicle] for vehicle in self.vehicles]
        return next_locations

    def is_local_in_intersection(self, location):
        """
        Takes a local coordinate and returns whether or not it is on the road
        :param location:
        :return:
        """
        # Checking if something is in a circle centered at the origin is so pleasant
        result = (math.sqrt(math.pow(location[0], 2) + math.pow(location[1], 2)) < self.radius)
        return result

    def is_global_on_road(self, location):
        """
        Takes a global coordinate and returns whether or not it is on the road
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

        return

    def update_positions(self):
        """
        Updates the position of each vehicle on the intersection.
        :return:
        """

        return

    def process_collisions(self):
        """
        Discovers which vehicles have crashed and informs them.
        :return:
        """

        locations = [vehicle.get_location() for vehicle in self.vehicles]

        for vehicle_index in self.list_duplicates(locations):
            self.vehicles[vehicle_index].crash()

        return

    def list_duplicates(self, seq):
        """
        Helper method for process_collisions
        :param seq:
        :return:
        """
        tally = defaultdict(list)
        for i, item in enumerate(seq):
            tally[item].append(i)
        return ((key, locs) for key, locs in tally.items() if len(locs) > 1)

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

        return