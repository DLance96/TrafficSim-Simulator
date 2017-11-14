import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.SimulationController import SimulationController
from src.TrafficMap import TrafficMap
from src.Road import Road
from src.Intersection import Intersection
from src.drivers.DriverTemplate import  DriverTemplate
from src.vehicles.VehicleTemplate import VehicleTemplate
from src.drivers.DriverTemplate import SpeedoFerraro
from src.drivers.DriverTemplate import SlowDriver
from src.vehicles.VehicleTemplate import Ferrari

trafficmap = TrafficMap()
onlyroad = Road([200,200], 1000, 2, 2, 0, 50, .01)
initial_intersection = Intersection(center = (200, 220), radius = 30, speed_limit = 200)
terminal_intersection = Intersection(center = (1200, 220), radius = 30, speed_limit = 200)
onlyroad.add_neighboring_intersection(initial_intersection, 'initial')
onlyroad.add_neighboring_intersection(terminal_intersection, 'terminal')
trafficmap.roadlist.append(onlyroad)
trafficmap.intersectionlist.append(initial_intersection)
trafficmap.intersectionlist.append(terminal_intersection)
controller = SimulationController(trafficmap, 20, 100, 60)
onlyroad.spawn(Ferrari(), SpeedoFerraro(), "outbound", initx=0, laneno=0)
onlyroad.spawn(VehicleTemplate(), SlowDriver(), "outbound", initx=500, laneno=0)
onlyroad.spawn(Ferrari(), SpeedoFerraro(), "inbound", initx=0, laneno=0)
onlyroad.spawn(VehicleTemplate(), SlowDriver(), "inbound", initx=500, laneno=0)

#onlyroad.spawn(VehicleTemplate(), DriverTemplate(), "inbound")
controller.run()
