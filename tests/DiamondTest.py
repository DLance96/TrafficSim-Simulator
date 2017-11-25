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
upper_right_road = Road([430, 50], 460, 2, 2, math.pi / 4, 50, .01)
lower_right_road = Road([753, 433], 460, 2, 2, 3 * math.pi / 4, 50, .01)
lower_left_road = Road([370, 50 + 2 * 353], 460, 2, 2, 5 * math.pi / 4, 50, .01)
upper_left_road = Road([47, 373], 460, 2, 2, 7 * math.pi / 4, 50, .01)

# Create the 4 intersections
upper_intersection = Intersection(center = (400, 50), radius = 30, speed_limit = 200)
right_intersection = Intersection(center = (400 + 353, 50 + 353), radius = 30, speed_limit = 200)
lower_intersection = Intersection(center = (400, 50 + 2 * 353), radius = 30, speed_limit = 200)
left_intersection = Intersection(center = (400 - 353, 50 + 353), radius = 30, speed_limit = 200)

# For each of the roads add the appropriate neighboring intersections
lower_left_road.add_neighboring_intersection(left_intersection, 'initial')
lower_left_road.add_neighboring_intersection(lower_intersection, 'terminal')

lower_right_road.add_neighboring_intersection(lower_intersection, 'initial')
lower_right_road.add_neighboring_intersection(right_intersection, 'terminal')

upper_right_road.add_neighboring_intersection(right_intersection, 'initial')
upper_right_road.add_neighboring_intersection(upper_intersection, 'terminal')

upper_left_road.add_neighboring_intersection(upper_intersection, 'initial')
upper_left_road.add_neighboring_intersection(left_intersection, 'terminal')

# For each of the intersections add the appropriate neighboring roads
left_intersection.add_neighboring_road(lower_left_road, 'initial')
left_intersection.add_neighboring_road(upper_left_road, 'terminal')

lower_intersection.add_neighboring_road(lower_left_road, 'terminal')
lower_intersection.add_neighboring_road(lower_right_road, 'initial')

right_intersection.add_neighboring_road(upper_right_road, 'initial')
right_intersection.add_neighboring_road(lower_right_road, 'terminal')

upper_intersection.add_neighboring_road(upper_right_road, 'terminal')
upper_intersection.add_neighboring_road(upper_left_road, 'initial')

# Add the roads to the trafficmap
trafficmap.roadlist.append(lower_left_road)
trafficmap.roadlist.append(lower_right_road)
trafficmap.roadlist.append(upper_right_road)
trafficmap.roadlist.append(upper_left_road)

# Add the intersections to the trafficmap
trafficmap.intersectionlist.append(left_intersection)
trafficmap.intersectionlist.append(lower_intersection)
trafficmap.intersectionlist.append(upper_intersection)
trafficmap.intersectionlist.append(right_intersection)

controller = SimulationController(trafficmap, 200, 200, 60)

# Spawn some cars
lower_left_road.spawn(VehicleTemplate(), DriverTemplate(), "outbound")
lower_left_road.spawn(VehicleTemplate(), DriverTemplate(), "inbound")

lower_right_road.spawn(VehicleTemplate(), DriverTemplate(), "outbound")
lower_right_road.spawn(VehicleTemplate(), DriverTemplate(), "inbound")

upper_right_road.spawn(VehicleTemplate(), DriverTemplate(), "outbound")
upper_right_road.spawn(VehicleTemplate(), DriverTemplate(), "inbound")
upper_left_road.spawn(VehicleTemplate(), DriverTemplate(), "outbound")
upper_left_road.spawn(VehicleTemplate(), DriverTemplate(), "inbound")


controller.run()