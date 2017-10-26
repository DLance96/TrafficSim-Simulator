
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

        return self.alive


    def set_previous_bucket(self, bucket):

        self.previous_bucket = bucket

        return

    def set_next_bucket(self, bucket):

        self.next_bucket = bucket

        return

    def set_previous_alive_bucket(self, bucket):

        self.previous_alive_bucket = bucket

        return

    def set_next_alive_bucket(self):

        self.next_alive_bucket = bucket

        return

    def get_previous_bucket(self):

        return self.previous_bucket

    def get_next_bucket(self):

        return self.next_bucket

    def get_previous_alive_bucket(self):

        return self.previous_alive_bucket

    def get_next_alive_bucket(self):

        return self.next_alive_bucket

    def add(self, vehicle):

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

            # seek the previous live bucket
            prev = self.prev_bucket
            while((prev is not None) and not prev.is_alive()):
                prev = prev.get_previous_bucket()
            self.previous_alive_bucket = prev

        return

    def remove(self, vehicle):

        self.vehicles.remove(vehicle)
        self.number_of_vehicles -= 1
        if self.number_of_vehicles == 0:
            # Process of becoming dead
            self.alive = False
            self.previous_alive_bucket.set_next_alive_bucket(self.next_alive_bucket)
            self.next_alive_bucket.set_previous_alive_bucket(self.previous_alive_bucket)
            self.next_alive_bucket = None
            self.previous_alive_bucket = None

        return

    def get_vehicles(self):

        return self.vehicles



