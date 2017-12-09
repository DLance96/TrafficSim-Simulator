import random
from src.drivers.DriverTemplate import *
from src.vehicles.VehicleTemplate import *
from src.Reporter import Reporter

class TrafficMap:
    """
    :type roadlist: list(Road)
    """
    def __init__(self, reporter = Reporter()):

        self.roadlist = []
        self.intersectionlist = []
        self.reporter = reporter

    def add_road(self, road):
        """
        Adds a Road to the traffic map
        :param road:
        :return:
        """
        # roads need to be assigned unique names for the reporter
        road.set_name(len(self.roadlist))
        # pass the reporter to the road so it knows where to report
        road.set_reporter(self.reporter)
        # create an entry for the road in the reporter with the same name as the road
        self.reporter.create_road_entry(len(self.roadlist))
        # add the road to the trafficmap's list of roads
        self.roadlist.append(road)
        return

    def add_intersection(self, intersection):
        """
        Adds an intersection to the traffic map
        :param intersection:
        :return:
        """
        # intersections need to be assigned unique names for the reporter
        intersection.set_name(len(self.intersectionlist))
        # pass the reporter to the intersection so it knows where to report
        intersection.set_reporter(self.reporter)
        # create an entry for the intersection in the reporter
        self.reporter.create_intersection_entry(len(self.intersectionlist))
        # add the intersection to the intersection list
        self.intersectionlist.append(intersection)

    def get_roads(self):
        """
        :return: a list of all roads in the map
        :rtype: list(Road)
        """
        return self.roadlist

    def get_intersections(self):
        """
        :return: list of all intersections in the map
        :rtype: list(Road)
        """
        return self.intersectionlist

    def tick(self, ticktime_ms):
        """
        Instruct each environment object (Road/Intersection) to perform the tick step for each of their vehicles
        :type ticktime_ms: float
        :return: None
        """
        for i in range(len(self.roadlist)):
            self.roadlist[i].tick(ticktime_ms)

        for i in range(len(self.intersectionlist)):
            self.intersectionlist[i].tick(ticktime_ms)

    def tock(self, ticktime_ms):
        """
        Instruct each environment object (Road/Intersection) to perform the two tock steps on each of their vehicles
        :type ticktime_ms: float
        :return:
        """
        for i in range(len(self.roadlist)):
            self.roadlist[i].tock_positions()

        for i in range(len(self.intersectionlist)):
            self.intersectionlist[i].tock_positions()

        for i in range(len(self.roadlist)):
            self.roadlist[i].tock_crashes()

        for i in range(len(self.intersectionlist)):
            self.intersectionlist[i].tock_crashes()