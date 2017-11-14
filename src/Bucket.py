
class Bucket:
    """
    has list of vehicles
    has alive boolean
    has location (in x only)
    has nextlive *
    has prevlive *
    has length
    """

    lane_width = 10

    def __init__(self, initial_x, length, inbound_lanes, outbound_lanes):
        """
        :param anchor_corner: [double, double]
        :param length: double
        :param inbound_lanes: int
        :param outbound_lanes: int
        :param orientatino: double (IN RADIANS!)
        :param speed_limit: int
        """
        self.length = length
        self.inbound_lanes = inbound_lanes
        self.outbound_lanes = outbound_lanes
        self.previous_bucket = None
        self.next_bucket = None
        self.next_alive_bucket = None
        self.previous_alive_bucket = None
        self.x_range = [initial_x, initial_x + length]
        self.outbound_y_range = [0, self.lane_width * outbound_lanes]
        self.inbound_y_range = [self.lane_width * outbound_lanes,
                                self.lane_width * outbound_lanes + self.lane_width * inbound_lanes]
        self.vehicles = []
        self.number_of_vehicles = 0
        self.alive = False

    def is_alive(self):
        """
        Returns the aliveness status of the Bucket. Used to limit computation when vehicles seek nearby vehicles.
        :return:
        """

        return self.alive


    def set_previous_bucket(self, bucket):
        """
        Sets the previous_bucket variable
        :param bucket:
        :return:
        """

        self.previous_bucket = bucket

        return

    def set_next_bucket(self, bucket):
        """
        Sets the next_bucket variable
        :param bucket:
        :return:
        """

        self.next_bucket = bucket

        return

    def set_previous_alive_bucket(self, bucket):
        """
        Sets the previous_alive_bucket variable
        :param bucket:
        :return:
        """

        self.previous_alive_bucket = bucket

        return

    def set_next_alive_bucket(self, bucket):
        """
        Sets the next_alive_bucket variable
        :return:
        """

        self.next_alive_bucket = bucket

        return

    def get_previous_bucket(self):
        """
        Gets the previous_bucket variable
        :return:
        """

        return self.previous_bucket

    def get_next_bucket(self):
        """
        Gets the next_bucket variable
        :return:
        """

        return self.next_bucket

    def get_previous_alive_bucket(self):
        """
        Gets the previous_alive_bucket variable
        :return:
        """

        return self.previous_alive_bucket

    def get_next_alive_bucket(self):
        """
        Gets the next_alive_bucket variable
        :return:
        """

        return self.next_alive_bucket

    def add(self, vehicle):
        """
        Adds the provided vehicle to the Bucket, replacing the vehicle's existing Bucket
        variable with this Bucket. Updates aliveness and the aliveness linked list.
        :param vehicle:
        :return:
        """

        self.vehicles.append(vehicle)
        self.number_of_vehicles += 1
        if self.number_of_vehicles == 1:
            self.alive = True

            # Process becoming alive

            # seek the next live bucket
            next = self.next_bucket
            while((next is not None) and not next.is_alive()):
                next = next.get_next_bucket()
            self.next_alive_bucket = next
            if next is not None:
                next.set_previous_alive_bucket(self)

            # seek the previous live bucket
            prev = self.previous_bucket
            while((prev is not None) and not prev.is_alive()):
                prev = prev.get_previous_bucket()
            self.previous_alive_bucket = prev
            if prev is not None:
                prev.set_next_alive_bucket(self)

        return

    def remove(self, vehicle):
        """
        Removes the provided vehicle from the Bucket. Updates aliveness and the aliveness linked list.
        :param vehicle:
        :return:
        """

        self.vehicles.remove(vehicle)
        self.number_of_vehicles -= 1
        if self.number_of_vehicles == 0:
            # Process of becoming dead
            self.alive = False
            if self.previous_alive_bucket is not None:
                self.previous_alive_bucket.set_next_alive_bucket(self.next_alive_bucket)
            if self.next_alive_bucket is not None:
                self.next_alive_bucket.set_previous_alive_bucket(self.previous_alive_bucket)
            self.next_alive_bucket = None
            self.previous_alive_bucket = None

        return

    def get_vehicles(self):
        """
        Gets the list of vehicles currently in the Bucket
        :return:
        """

        return self.vehicles