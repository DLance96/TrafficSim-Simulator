import random
from src.drivers.DriverTemplate import *
from src.vehicles.VehicleTemplate import *

class TrafficMap:
    """
    :type roadlist: list(Road)
    """
    def __init__(self):

        self.roadlist = []
        self.intersectionlist = []

    def add_road(self, road):
        road.set_name(len(self.roadlist))
        self.roadlist.append(road)
        return

    def add_intersection(self, intersection):
        intersection.set_name(len(self.intersectionlist))
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
        :type ticktime_ms: float
        :return: None
        """
        for i in range(len(self.roadlist)):
            self.roadlist[i].tick(ticktime_ms)

        for i in range(len(self.intersectionlist)):
            self.intersectionlist[i].tick(ticktime_ms)

    def tock(self, ticktime_ms):
        """
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