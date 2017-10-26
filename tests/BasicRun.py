from SimulationController import SimulationController
from TrafficMap import TrafficMap
from Road import Road
from Intersection import Intersection
from drivers.DriverTemplate import  DriverTemplate
from vehicles.VehicleTemplate import VehicleTemplate

trafficmap = TrafficMap()
onlyroad = Road([200,200],200, 2, 2, 0, 200)
initial_intersection = Intersection(center = (200, 215), radius = 15, speed_limit = 200)
terminal_intersection = Intersection(center = (400, 415), radius = 15, speed_limit = 200)
onlyroad.add_neighboring_intersection(initial_intersection, 'initial')
onlyroad.add_neighboring_intersection(terminal_intersection, 'terminal')
trafficmap.roadlist.append(onlyroad)
controller = SimulationController(trafficmap, 20, -1, 60)
onlyroad.spawn(VehicleTemplate(), DriverTemplate(), 0)
controller.run()
