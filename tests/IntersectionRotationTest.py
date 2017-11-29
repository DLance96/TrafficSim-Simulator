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
onlyroad = Road([400,200], 600, 2, 2, 3.14/10, 50)
initial_intersection = Intersection(center = (200, 220), radius = 300, speed_limit = 200)
terminal_intersection = Intersection(center = (1100, 220), radius = 300, speed_limit = 200)
initial_intersection.bind_road_to_intersection(onlyroad,'terminal')
terminal_intersection.bind_road_to_intersection(onlyroad,'initial')
trafficmap.roadlist.append(onlyroad)
trafficmap.intersectionlist.append(initial_intersection)
trafficmap.intersectionlist.append(terminal_intersection)
controller = SimulationController(trafficmap, 20, 100, 60)
onlyroad.spawn(Ferrari(), SpeedoFerraro(), "outbound", initx=0, laneno=0)
onlyroad.spawn(VehicleTemplate(), SlowDriver(), "outbound", initx=500, laneno=0)
#onlyroad.spawn(Ferrari(), SpeedoFerraro(), "inbound", initx=0, laneno=0)
#onlyroad.spawn(VehicleTemplate(), SlowDriver(), "inbound", initx=500, laneno=0)

#onlyroad.spawn(VehicleTemplate(), DriverTemplate(), "inbound")
controller.run()
