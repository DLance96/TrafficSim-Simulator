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

# Create the trafficmap
trafficmap = TrafficMap()

# Create the four roads
lower_road = Road([120, 620], 500, 2, 2, 0, 50, .01)
right_road = Road([620, 620], 500, 2, 2, 3 * math.pi / 2, 50, .01)
upper_road = Road([620, 120], 500, 2, 2, math.pi, 50, .01)
left_road = Road([120, 120], 500, 2, 2, math.pi / 2, 50, .01)

# Create the 4 intersections
lower_left_intersection = Intersection(center = (100, 640), radius = 30, speed_limit = 200)
lower_right_intersection = Intersection(center = (640, 640), radius = 30, speed_limit = 200)
upper_left_intersection = Intersection(center = (100, 100), radius = 30, speed_limit = 200)
upper_right_intersection = Intersection(center = (640, 100), radius = 30, speed_limit = 200)

# For each of the roads add the appropriate neighboring intersections
lower_road.add_neighboring_intersection(lower_left_intersection, 'initial')
lower_road.add_neighboring_intersection(lower_right_intersection, 'terminal')

right_road.add_neighboring_intersection(lower_right_intersection, 'initial')
right_road.add_neighboring_intersection(upper_right_intersection, 'terminal')

upper_road.add_neighboring_intersection(upper_right_intersection, 'initial')
upper_road.add_neighboring_intersection(upper_left_intersection, 'terminal')

left_road.add_neighboring_intersection(upper_left_intersection, 'initial')
left_road.add_neighboring_intersection(lower_left_intersection, 'terminal')

# For each of the intersections add the appropriate neighboring roads
lower_left_intersection.add_neighboring_road(lower_road)
lower_left_intersection.add_neighboring_road(left_road)

lower_right_intersection.add_neighboring_road(lower_road)
lower_right_intersection.add_neighboring_road(right_road)

upper_right_intersection.add_neighboring_road(upper_road)
upper_right_intersection.add_neighboring_road(right_road)

upper_left_intersection.add_neighboring_road(upper_road)
upper_left_intersection.add_neighboring_road(left_road)

# Add the roads to the trafficmap
trafficmap.roadlist.append(lower_road)
trafficmap.roadlist.append(right_road)
trafficmap.roadlist.append(upper_road)
trafficmap.roadlist.append(left_road)

# Add the intersections to the trafficmap
trafficmap.intersectionlist.append(lower_left_intersection)
trafficmap.intersectionlist.append(lower_right_intersection)
trafficmap.intersectionlist.append(upper_left_intersection)
trafficmap.intersectionlist.append(upper_right_intersection)

controller = SimulationController(trafficmap, 20, 100, 60)

# Spawn some cars
lower_road.spawn(VehicleTemplate(), DriverTemplate(), "outbound")
lower_road.spawn(VehicleTemplate(), DriverTemplate(), "inbound")

right_road.spawn(VehicleTemplate(), DriverTemplate(), "outbound")
right_road.spawn(VehicleTemplate(), DriverTemplate(), "inbound")

upper_road.spawn(VehicleTemplate(), DriverTemplate(), "outbound")
upper_road.spawn(VehicleTemplate(), DriverTemplate(), "inbound")

left_road.spawn(VehicleTemplate(), DriverTemplate(), "outbound")
left_road.spawn(VehicleTemplate(), DriverTemplate(), "inbound")


controller.run()