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


def test_traffic_cycle():
    # Create the trafficmap
    trafficmap = TrafficMap()

    # Create the TemplatePairFactory prebuilt list for the intersections
    prebuilt_list = [((0, 1), DriverTemplate(),VehicleTemplate())]

    # Create the four roads
    upper_right_road = Road([430, 50], 460, 2, 2, math.pi / 4, 50)
    lower_right_road = Road([753, 433], 460, 2, 2, 3 * math.pi / 4, 50)
    lower_left_road = Road([370, 50 + 2 * 353], 460, 2, 2, 5 * math.pi / 4, 50)
    upper_left_road = Road([47, 373], 460, 2, 2, 7 * math.pi / 4, 50)

    # Create the 4 intersections
    upper_intersection = Intersection(center = (400, 50), radius = 30, speed_limit = 200,
                                      template_factory = TemplatePairFactory(1000, prebuilt_list),
                                      traffic_cycle = TrafficCycle(green_lights = [[0], [1]], timings = [20000, 20000],
                                                                   yellow_light_length = 6000))
    right_intersection = Intersection(center = (400 + 353, 50 + 353), radius = 30, speed_limit = 200,
                                      template_factory = TemplatePairFactory(1000, prebuilt_list),
                                      traffic_cycle=TrafficCycle(green_lights=[[0], [1]], timings=[20000, 20000],
                                                                 yellow_light_length=6000))
    lower_intersection = Intersection(center = (400, 50 + 2 * 353), radius = 30, speed_limit = 200,
                                      template_factory = TemplatePairFactory(1000, prebuilt_list),
                                      traffic_cycle=TrafficCycle(green_lights=[[0], [1]], timings=[20000, 20000],
                                                                 yellow_light_length=6000))
    left_intersection = Intersection(center = (400 - 353, 50 + 353), radius = 30, speed_limit = 200,
                                     template_factory = TemplatePairFactory(1000, prebuilt_list),
                                     traffic_cycle=TrafficCycle(green_lights=[[0], [1]], timings=[20000, 20000],
                                                                yellow_light_length=6000))

    # For each of the intersections add the appropriate neighboring roads
    left_intersection.bind_road_to_intersection(lower_left_road, 'terminal')
    left_intersection.bind_road_to_intersection(upper_left_road, 'initial')

    lower_intersection.bind_road_to_intersection(lower_left_road, 'initial')
    lower_intersection.bind_road_to_intersection(lower_right_road, 'terminal')

    right_intersection.bind_road_to_intersection(upper_right_road, 'terminal')
    right_intersection.bind_road_to_intersection(lower_right_road, 'initial')

    upper_intersection.bind_road_to_intersection(upper_right_road, 'initial')
    upper_intersection.bind_road_to_intersection(upper_left_road, 'terminal')

    # Add the roads to the trafficmap
    trafficmap.add_road(lower_left_road)
    trafficmap.add_road(lower_right_road)
    trafficmap.add_road(upper_right_road)
    trafficmap.add_road(upper_left_road)

    # Add the intersections to the trafficmap
    trafficmap.add_intersection(left_intersection)
    trafficmap.add_intersection(lower_intersection)
    trafficmap.add_intersection(upper_intersection)
    trafficmap.add_intersection(right_intersection)

    controller = SimulationController(trafficmap, 200, 60, 60)

    controller.run()

