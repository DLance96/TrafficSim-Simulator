import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import traceback
from src.SimulationController import SimulationController
from src.TrafficMap import TrafficMap
from src.Road import Road
from src.Intersection import Intersection
from src.drivers.DriverTemplate import  DriverTemplate
from src.vehicles.VehicleTemplate import VehicleTemplate
from src.TemplatePairFactory import TemplatePairFactory

def basic_run():
    trafficmap = TrafficMap()
    prebuilt_list = [((0, 1), DriverTemplate(),VehicleTemplate())]
    onlyroad = Road([200,200], 800, 2, 2, 0, 100)

    initial_intersection = Intersection(center = (100, 220), radius = 130, speed_limit = 10,
                                        template_factory=TemplatePairFactory(10000, prebuilt_list))
    terminal_intersection = Intersection(center = (1100, 220), radius = 130, speed_limit = 10,
                                         template_factory=TemplatePairFactory(10000, prebuilt_list))
    initial_intersection.bind_road_to_intersection(onlyroad,'initial')
    terminal_intersection.bind_road_to_intersection(onlyroad,'terminal')
    trafficmap.roadlist.append(onlyroad)
    trafficmap.intersectionlist.append(initial_intersection)
    trafficmap.intersectionlist.append(terminal_intersection)
    controller = SimulationController(trafficmap, 20, 60, 30)

    controller.run()

