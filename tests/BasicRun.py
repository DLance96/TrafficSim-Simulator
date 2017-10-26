from SimulationController import SimulationController
from TrafficMap import TrafficMap
from Road import Road
from Intersection import Intersection
from drivers.DriverTemplate import  DriverTemplate
from vehicles.VehicleTemplate import VehicleTemplate

trafficmap = TrafficMap()
onlyroad = Road([200,200],200, 2, 2, 0, 200)
initial_intersection = Intersection(center = (200, 220), radius = 30, speed_limit = 200)
terminal_intersection = Intersection(center = (400, 220), radius = 30, speed_limit = 200)
onlyroad.add_neighboring_intersection(initial_intersection, 'initial')
onlyroad.add_neighboring_intersection(terminal_intersection, 'terminal')
trafficmap.roadlist.append(onlyroad)
trafficmap.intersectionlist.append(initial_intersection)
trafficmap.intersectionlist.append(terminal_intersection)
controller = SimulationController(trafficmap, 20, 10, 60)
onlyroad.spawn(VehicleTemplate(), DriverTemplate(), 0)
controller.run()
