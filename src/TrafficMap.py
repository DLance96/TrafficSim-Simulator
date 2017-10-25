
class TrafficMap:

    def __init__(self):
        """
        """
        self.roadlist = []
        self.intersectionlist = []

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