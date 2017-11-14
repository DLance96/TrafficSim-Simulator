import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.SimulationController import SimulationController
from src.TrafficMap import TrafficMap
from src.Road import Road
from src.Intersection import Intersection
from src.drivers.DriverTemplate import  DriverTemplate
from src.vehicles.VehicleTemplate import VehicleTemplate

trafficmap = TrafficMap()
toproad = Road([200,200], 500, 2, 2, 0, 50, .01)
bottomroad = Road([200,200], 500, 2, 2, 0, 50, .01)
leftroad = Road([200,200], 500, 2, 2, 0, 50, .01)
rightroad = Road([200,200], 500, 2, 2, 0, 50, .01)
topleft_intersection = Intersection(center = (200, 220), radius = 30, speed_limit = 200)
topright_intersection = Intersection(center = (200, 220), radius = 30, speed_limit = 200)
bottomleft_intersection = Intersection(center = (700, 220), radius = 30, speed_limit = 200)
bottomright_intersection = Intersection(center = (700, 220), radius = 30, speed_limit = 200)
onlyroad.add_neighboring_intersection(initial_intersection, 'initial')
onlyroad.add_neighboring_intersection(terminal_intersection, 'terminal')
trafficmap.roadlist.append(onlyroad)
trafficmap.intersectionlist.append(initial_intersection)
trafficmap.intersectionlist.append(terminal_intersection)
controller = SimulationController(trafficmap, 200, 100, 60)
onlyroad.spawn(VehicleTemplate(), DriverTemplate(), "outbound")
onlyroad.spawn(VehicleTemplate(), DriverTemplate(), "outbound")
controller.run()