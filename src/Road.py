
"""
TODO:
add tick method s.t. calling tick will advance the simulation 1 tick
implement Bucket list iterator
"""
class Road:

    lane_width = 3

    def __init__(self,length, width, speed_limit, lanes):
        """
        :param length: int
        :param width: int
        :param speed_limit: int
        :param lanes: int
        """
        self.length = length
        self.width = width
        self.speed_limit = speed_limit
        self.lanes = lanes

    def tick(self):
        """
        stuff here
        """

class Bucket_Iterator:
    """
    TODO:
    add getnext() (which also iterates to the next vehicle)
    getnext returns Null if there are no vehicle left
    """