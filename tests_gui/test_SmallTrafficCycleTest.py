import sys
import os
import math
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.SimulationController import SimulationController
from src.TrafficMap import TrafficMap
from src.Road import Road
from src.Intersection import Intersection
from src.drivers.DriverTemplate import  DriverTemplate
from src.vehicles.VehicleTemplate import VehicleTemplate
from src.TemplatePairFactory import TemplatePairFactory
from src.TrafficCycle import TrafficCycle


# Create the trafficmap
trafficmap = TrafficMap()

# Create the TemplatePairFactory prebuilt list for the intersections
prebuilt_list = [((0, 1), DriverTemplate(),VehicleTemplate())]

def test_small_traffic_cycle():
    onlyroad = Road([220,200], 760, 2, 2, 0, 50)

    initial_intersection = Intersection(center = (200, 220), radius = 30, speed_limit = 200,
                                        template_factory=TemplatePairFactory(10000, prebuilt_list),
                                        traffic_cycle=TrafficCycle(green_lights=[[0], [1]], timings=[20000, 20000],
                                                                   yellow_light_length=6000))
    terminal_intersection = Intersection(center = (1000, 220), radius = 30, speed_limit = 200,
                                         template_factory=TemplatePairFactory(10000, prebuilt_list),
                                        traffic_cycle = TrafficCycle(green_lights=[[0], [1]], timings=[20000, 20000],
                                                                     yellow_light_length=6000))
    initial_intersection.bind_road_to_intersection(onlyroad,'initial')
    terminal_intersection.bind_road_to_intersection(onlyroad,'terminal')

    trafficmap.add_road(onlyroad)
    trafficmap.add_intersection(initial_intersection)
    trafficmap.add_intersection(terminal_intersection)

    controller = SimulationController(trafficmap, 200, 60, 60)

    controller.run()

