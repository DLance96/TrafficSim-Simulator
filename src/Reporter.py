import time
import operator
import random
import math
from src.vehicles.VehicleTemplate import VehicleTemplate
from src.drivers.DriverTemplate import DriverTemplate


class Reporter:
    class Report:

        def __init__(self):
            self.number_of_vehicles = []
            self.average_speed = []
            self.number_of_crashes = []

        def read(self):
            return self.number_of_vehicles, self.average_speed, self.number_of_crashes

    def __init__(self, ):

        self.report_table = {}


