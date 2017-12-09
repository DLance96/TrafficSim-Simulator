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

def test_square():
    # Create the trafficmap
    trafficmap = TrafficMap()

    prebuilt_list = [((0, 1), DriverTemplate(),VehicleTemplate())]

    # Create the four roads
    lower_road = Road([120, 620], 500, 2, 2, 0, 50)
    right_road = Road([620, 620], 500, 2, 2, 3 * math.pi / 2, 50)
    upper_road = Road([620, 120], 500, 2, 2, math.pi, 50)
    left_road = Road([120, 120], 500, 2, 2, math.pi / 2, 50)

    # Create the 4 intersections
    lower_left_intersection = Intersection(center = (100, 640), radius = 30, speed_limit = 200,
                                           template_factory=TemplatePairFactory(1000, prebuilt_list))
    lower_right_intersection = Intersection(center = (640, 640), radius = 30, speed_limit = 200,
                                            template_factory=TemplatePairFactory(1000, prebuilt_list))
    upper_left_intersection = Intersection(center = (100, 100), radius = 30, speed_limit = 200,
                                           template_factory = TemplatePairFactory(1000, prebuilt_list))
    upper_right_intersection = Intersection(center = (640, 100), radius = 30, speed_limit = 200,
                                            template_factory = TemplatePairFactory(1000, prebuilt_list))

    # For each of the intersections add the appropriate neighboring roads
    lower_left_intersection.bind_road_to_intersection(lower_road, 'initial')
    lower_left_intersection.bind_road_to_intersection(left_road, 'terminal')

    lower_right_intersection.bind_road_to_intersection(lower_road, 'terminal')
    lower_right_intersection.bind_road_to_intersection(right_road, 'initial')

    upper_right_intersection.bind_road_to_intersection(upper_road, 'initial')
    upper_right_intersection.bind_road_to_intersection(right_road, 'terminal')

    upper_left_intersection.bind_road_to_intersection(upper_road, 'terminal')
    upper_left_intersection.bind_road_to_intersection(left_road, 'initial')

    # Add the roads to the trafficmap
    trafficmap.add_road(lower_road)
    trafficmap.add_road(right_road)
    trafficmap.add_road(upper_road)
    trafficmap.add_road(left_road)

    # Add the intersections to the trafficmap
    trafficmap.add_intersection(lower_left_intersection)
    trafficmap.add_intersection(lower_right_intersection)
    trafficmap.add_intersection(upper_left_intersection)
    trafficmap.add_intersection(upper_right_intersection)

    controller = SimulationController(trafficmap, 200, 60, 60)

    controller.run()

test_square() # pragma: no cover