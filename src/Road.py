import math
import random
from collections import defaultdict
from shapely import geometry
from Bucket import Bucket
from Vehicle import Vehicle

class Road:

    lane_width = 10

    def __init__(self, anchor_corner, length, inbound_lanes, outbound_lanes, orientation, speed_limit):
        """
        :param anchor_corner: [double, double]
        :param length: double
        :param inbound_lanes: int
        :param outbound_lanes: int
        :param orientatino: double (IN RADIANS!)
        :param speed_limit: int
        """
        self.anchor = anchor_corner
        self.length = length
        self.inbound_lanes = inbound_lanes
        self.outbound_lanes = outbound_lanes
        self.lanes = inbound_lanes + outbound_lanes
        self.width = self.lanes * self.lane_width
        self.orientation = orientation
        self.speed_limit = speed_limit
        self.bucket_length = 0.2778 * self.speed_limit * 10
        self.initial_intersection = None
        self.terminal_intersection = None
        self.vehicles = []
        self.bucket_list = self.initialize_buckets(road_length = self.length,
                                          road_width = self.width,
                                          bucket_length = self.bucket_length,
                                          inbound_lanes = self.inbound_lanes,
                                          outbound_lanes = self.outbound_lanes)
        self.surface = self.generate_surface()
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

    def initialize_buckets(self, road_length, road_width, bucket_length, inbound_lanes, outbound_lanes):
        """
        Creates a list of buckets of length equal to 10 seconds of travel at the speed limit
        to populate the length of the road.
        :param road_length:
        :param road_width:
        :param bucket_length:
        :param inbound_lanes:
        :param outbound_lanes:
        :return:
        """

        number_of_buckets = math.ceil(road_length / bucket_length)
        bucket_list = []

        for i in range(number_of_buckets):

            if i == 0:
                head = Bucket(initial_x = i * self.bucket_length, length=bucket_length,
                              inbound_lanes=inbound_lanes, outbound_lanes=outbound_lanes)
                tail = head
                bucket_list.append(head)
            else:
                next = Bucket(intial_x = i * self.bucket_length, length=bucket_length,
                              inbound_lanes=inbound_lanes, outbound_lanes=outbound_lanes)
                next.set_previous_bucket(tail)
                tail.set_next_bucket(next)
                tail = next
                bucket_list.append(tail)

        return bucket_list

    def generate_surface(self):
        """
        Generates the shapely Polygon storing the surface of the road.
        :return:
        """
        # Points proceed clockwise around the rectangle from the anchor point
        # [x, y] formatting
        first = self.anchor
        second = [first[0] + self.length * math.cos(self.orientation), first[1] + self.length * math.sin(self.orientation)]
        third = [second[0] + self.width * math.cos(self.orientation + math.pi / 2), second[1] + self.width * math.sin(self.orientation + math.pi / 2)]
        fourth = [first[0] + self.width * math.cos(self.orientation + math.pi / 2), first[1] + self.width * math.sin(self.orientation + math.pi / 2)]
        # Reference : https://toblerity.org/shapely/manual.html#polygons
        return geometry.Polygon([first, second, third, fourth])

    def request_next_locations(self, ticktime_ms):
        """
        Produces the next intended location of each car.
        :param ticktime_ms:
        :return:
        """
        next_locations = [[vehicle.get_intended_position(ticktime_ms), vehicle] for vehicle in self.vehicles]
        return next_locations

    def is_local_on_road(self, location):
        """
        Takes a local coordinate and returns whether or not it is on the road
        :param location:
        :return:
        """
        location = self.local_to_global_location_conversion(location)
        return self.surface.contains(geometry.Point(location[0], location[1]))

    def is_global_on_road(self, location):
        """
        Takes a global coordinate and returns whether or not it is on the road
        :param location:
        :return:
        """
        return self.surface.contains(geometry.Point(location[0], location[1]))

    def local_to_global_location_conversion(self, location):
        """
        Turn a local coordinate into its corresponding global coordinate
        :param location:
        :return:
        """

        x = self.anchor[0] + location[0] * math.cos(self.orientation) + location[1] * math.cos(self.orientation + math.pi / 2)
        y = self.anchor[1] + location[0] * math.sin(self.orientation) + location[1] * math.sin(self.orientation + math.pi / 2)

        return [x, y]

    def global_to_local_location_conversion(self, location):
        """
        Turn a global coordinate into its corresponding local coordinate
        :param location:
        :return:
        """

        # Recenter so that the anchor is the origin
        relative_x = location[0] - self.anchor[0]
        relative_y = location[1] - self.anchor[1]
        # Rotate counterclockwise by the orientation
        local_x = relative_x * math.cos(-self.orientation) - relative_y * math.sin(-self.orientation)
        local_y = relative_y * math.cos(-self.orientation) + relative_y * math.sin(-self.orientation)

        return [local_x, local_y]

    def which_neighbor(self, location):
        """
        akes a global coordinate and returns which, if any of the neighboring intersections contains that coordinate
        :param location:
        :return:
        """

        if self.initial_intersection.is_global_in_intersection(self.local_to_global_location_conversion(location)):
            return self.initial_intersection
        elif self.terminal_intersection.is_global_in_intersection(self.local_to_global_location_conversion(location)):
            return self.terminal_intersection
        else:
            raise ValueError("No neighbor contains that location.")
            return

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
        Takes a vehicle and a global coordinate and places the vehicle onto the road at the local coordinate
        corresponding to the global coordinate
        :param vehicle:
        :param location:
        :return:
        """

        local_location = self.global_to_local_location_conversion(location)
        vehicle.transfer_to_road(self, local_location)
        self.appropriately_bucket(vehicle, local_location)
        self.vehicles.append(vehicle)

        return


    def appropriately_bucket(self, vehicle, location):
        """
        Takes a vehicle and a local location and ensures that the vehicle is in the bucket corresponding to the location
        :param vehicle:
        :param location:
        :return:
        """

        # Remove the vehicle from its current bucket if it exists
        if vehicle.get_bucket() is not None:
            vehicle.get_bucket().remove(vehicle)
        # And place it into the new bucket in which it belongs
        bucket = self.bucket_list[math.floor(location[0] / self.bucket_length)]
        bucket.add(vehicle)
        # And inform the vehicle which bucket it is now in
        vehicle.set_bucket(bucket)

        return

    def update_positions(self):

        # Update the location of each vehicle by updating it directly or transferring it to a neighboring intersection
        for intended_location, vehicle in self.next_locations:
            if self.is_local_on_road(intended_location):
                vehicle.update_location(intended_location[0], intended_location[1])
                self.appropriately_bucket(vehicle, intended_location)
            else:
                global_location = self.local_to_global_location_conversion(intended_location)
                self.transfer(vehicle, global_location)

        # Reset the list of cars intending to move
        self.next_locations = []

        return

    # Thought about doing this bucket-wise, but can't. Vehicle can be in more than 1 bucket.
    def process_collisions(self):
        """
        Locates those vehicles which have been in a collision and informs them of that fact.
        :return:
        """

        locations = [vehicle.get_location() for vehicle in self.vehicles]
        # Actually need to get the actual sizes of cars to figure out if they have collided

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
        Takes the necessary inputs to generate a vehicle and attempts to generate the corresponding vehicles on a
        random lane at the beginning of the road driving outbound. If it would spawn on the same x-value as any
        existing vehicle, instead it is not spawned.
        :param vehicle_template:
        :param driver_template:
        :param direction:
        :return:
        """

        nearby_vehicles = self.bucket_list[0].get_vehicles()
        vehicle_length = vehicle_template.length
        clear = True
        # If the created vehicle were be adjacent to any vehicle, we don't want to spawn it
        # Later we could replace this with a direct collision check
        for vehicle in nearby_vehicles:
            if vehicle.get_location() - vehicle.get_cartype().length / 2 <= vehicle_length:
                clear = False

        if clear:
            # Pick a y location corresponding to the center of a random outbound lane
            y = (random.randint(0, self.outbound_lanes - 1) + .5) * self.lane_width
            # Pick an x location so that the car is just fully on the road
            x = vehicle_length / 2
            spawned_vehicle = Vehicle(self, x=x, y=y, vx=0, vy=0, orientation=self.orientation,
                                      cartype=vehicle_template, drivertype=driver_template)
            # Accepts a transfer from nowhere, kinda silly. Maybe rename accept_transfer for clarity?
            self.accept_transfer(spawned_vehicle, self.local_to_global_location_conversion((x, y)))

        return

    def add_neighboring_intersection(self, intersection, end):
        """
        Takes an intersection and an associated end of the road and adds that intersection at that road.
        :param intersection:
        :param end:
        :return:
        """
        if end == "initial":
            self.initial_intersection = intersection
        elif end == "terminal":
            self.terminal_intersection = intersection
        else:
            raise ValueError("Intersection added to an end other than 'initial' or 'terminal'")
        return