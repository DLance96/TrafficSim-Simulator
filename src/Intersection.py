import math
import itertools
from src.Surface import Surface
from src.Vehicle import Vehicle
from src.drivers.DriverTemplate import DriverTemplate
from src.vehicles.VehicleTemplate import VehicleTemplate
from itertools import repeat
from collections import defaultdict


class Intersection(Surface):

    lane_width = 10

    def __init__(self, center, radius, speed_limit, template_factory = None, traffic_cycle = None):
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
        self.spawning_profile = template_factory
        self.traffic_cycle = traffic_cycle
        # These lists are all same-indexed
        # Roads are ordered by orientation
        self.adjacent_roads = []
        self.adjacent_road_orientations = []
        self.adjacent_road_widths = []
        # List of tuples storing the bounds on the angle centered at the origin subtended by the road
        self.adjacent_road_bounding_orientations = []
        self.next_locations = [] # Prevents conflicts with cars being moved between tick and tock.
        self.name = None
        self.reporter = None
        # Does this intersection have a stoplight?
        # If there is a stoplight
        if self.traffic_cycle is not None:
            # Get the list of lights which are green and how long they will be green for.
            self.current_greens, self.time_until_transition = self.traffic_cycle.get_next()
            # Figure out how long lights will be yellow for
            self.yellow_duration = self.traffic_cycle.get_yellow_duration()
            # If the lights are created with less time than the yellow duration, the are created yellow (poor drivers)
            if self.time_until_transition <= self.yellow_duration:
                self.yellow = True
            else:
                self.yellow = False
        # If there is no stoplight
        else:
            # We can't set the current greens because we don't know at construction how many roads there will be
            # Obviously the lights are not yellow if they don't exist
            self.yellow = False

    def tick(self, ticktime_ms):
        """
        Performs the vehicle next location getting tick
        Spawns vehicles if appropriate
        :param ticktime_ms:
        :return:
        """
        # Process the traffic cycle, potentially changing green lights to yellow or which lights are green.
        if self.traffic_cycle is not None:
            self.time_until_transition -= ticktime_ms
            if self.time_until_transition <= 0:
                # Get the list of lights which are green and how long they will be green for.
                self.current_greens, self.time_until_transition = self.traffic_cycle.get_next()
            # Check if the lights should be yellow
            if self.time_until_transition <= self.yellow_duration:
                self.yellow = True
            else:
                self.yellow = False
        else:
            # All roads have a "green light" if there is no stoplight
            self.current_greens = range(len(self.adjacent_roads))
            # And obviously the lights are not yellow if they don't exist
            self.yellow = False

        self.next_locations = self.request_next_locations(ticktime_ms)

        if self.spawning_profile is not None:
            result = self.spawning_profile.prompt_spawn(ticktime_ms)
            if result is not None:
                # Code to implement converting the resulting vehicle and driver template into a vehicle
                # and placing it onto the intersection
                # Vehicles really need pathfinding so that they leave the intersection.
                # For now, vehicles are created in the middle of the intersection.
                self.spawn(result[0], result[1])

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
        Performs the crash detecting and handling tock, files the timestep report with the reporter
        :return:
        """

        crashes = self.process_collisions()
        if self.reporter is not None:
            number_of_vehicles = len(self.vehicles)
            if len(self.vehicles) > 0:
                avg_speed = sum([math.sqrt(v.vx ** 2 + v.vy ** 2) for v in self.vehicles]) / len(self.vehicles)
            else:
                avg_speed = "NAN"
            self.reporter.add_info_intersection(self.name, number_of_vehicles, avg_speed, crashes)

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
            print("A vehicle couldn't be transferred because it requested an invalid destination.")
            self.vehicles.remove(vehicle)

        return

    def accept_transfer(self, vehicle, location, road, side):
        """
        Takes a vehicle a global coordinate and the road the vehicle came from
        and places the vehicle at the local version of the coordinate.
        :param vehicle:
        :param location:
        :param road:
        :return:
        """
        road_orientation = road.orientation
        self.vehicles.append(vehicle)
        local_location = self.global_to_local_location_conversion(location)
        vehicle.transfer_to_intersection(self, local_location, road_orientation)

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
        count = 0
        vehicle_pairs = list(itertools.combinations(self.vehicles, 2))
        for (v1, v2) in vehicle_pairs:
            if self.have_collided(v1, v2):
                count += 1
                pass
                # I am assuming that vehicles will want to know which vehicle they collided with.
                v1.collided(v2)
                v2.collided(v1)

        return count

    def spawn(self, vehicle_template=VehicleTemplate(), driver_template=DriverTemplate()):
        """
        Takes the necessary inputs to generate a vehicle and attempts to generate the corresponding vehicles in the
        middle of the intersection in accordance with the spawning profile's frequency.
        If this would cause a collision, the vehicle is instead not spawned.
        :param vehicle_template:
        :param driver_template:
        :param direction:
        :param initx:
        :param laneno:
        :return:
        """

        spawned_vehicle = Vehicle(surface = self, x=0, y=0, vx=0, vy=0, orientation=0,
                                cartype = vehicle_template,
                                drivertype = driver_template)

        # Check to see if the spawned vehicle collides with any vehicles currently in the intersection
        spawning_collision = any(map(self.have_collided, self.vehicles, repeat(spawned_vehicle)))

        if not spawning_collision:
            self.vehicles.append(spawned_vehicle)

        return

    def debug_spawn(self, vehicle):
        self.vehicles.append(vehicle)

    def add_neighboring_road(self, road, side):
        """
        Takes a road and adds it to the intersection.
        This is assumed to be unable to fail, as non-physical roads should have errored before the simulation.
        :param road:
        :param side: informs the intersection if the road considers the intersection initial or terminal
        :return:
        """

        orientation = road.orientation if side == "terminal" else (road.orientation + math.pi) % (2 * math.pi)
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

    def bind_road_to_intersection(self, road, side):
        """
        Takes a road, an intersection, and which end of the road the intersection is and binds them together
        :param road:
        :param intersection:
        :param side: "initial" or "terminal"
        :return:
        """
        if side != "initial" and side != "terminal":
            raise ValueError("The two ends of a road are the 'initial' end and the 'terminal' end.")
        road.add_neighboring_intersection(self, side)
        self.add_neighboring_road(road, side)
        return

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_reporter(self, reporter):
        self.reporter = reporter

    def status_of_light(self, road):
        """
        Takes a road as an input and returns the status of the light for that road, "red", "yellow", or "green".
        If the road is not one of the roads attached to the intersection a ValueError is raised
        :param road:
        :return:
        """
        if road in self.adjacent_roads:
            index = self.adjacent_roads.index(road)
            if index in self.current_greens:
                if self.yellow:
                    return "yellow"
                else:
                    return "green"
            else:
                return "red"
        else:
            raise ValueError("The given road is not one of the roads attached to this intersection.")