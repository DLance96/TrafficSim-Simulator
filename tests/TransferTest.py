import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.SimulationController import SimulationController
from src.TrafficMap import TrafficMap
from src.Road import Road
from src.Vehicle import Vehicle
from src.Intersection import Intersection
from src.drivers.DriverTemplate import  DriverTemplate
from src.vehicles.VehicleTemplate import VehicleTemplate
from src.TemplatePairFactory import TemplatePairFactory
from src.drivers.DriverTemplate import SpeedoFerraro
from src.drivers.DriverTemplate import SlowDriver
from src.vehicles.VehicleTemplate import Ferrari

trafficmap = TrafficMap()
prebuilt_list = [((0, 1), DriverTemplate(),VehicleTemplate())]
onlyroad = Road([250,200], 700, 2, 2, 0, 50)

initial_intersection = Intersection(center = (200, 220), radius = 100, speed_limit = 200,
                                    template_factory = None)
terminal_intersection = Intersection(center = (1000, 220), radius = 100, speed_limit = 200,
                                     template_factory = None)
initial_intersection.bind_road_to_intersection(onlyroad,'initial')
terminal_intersection.bind_road_to_intersection(onlyroad,'terminal')
trafficmap.roadlist.append(onlyroad)
trafficmap.intersectionlist.append(initial_intersection)
trafficmap.intersectionlist.append(terminal_intersection)

spawned_vehicle_1 = Vehicle(surface = initial_intersection, x=0, y=10, vx=50, vy=0, orientation=0,
                                cartype = Ferrari(),
                                drivertype = SpeedoFerraro())
initial_intersection.debug_spawn(spawned_vehicle_1)
spawned_vehicle_2 = Vehicle(surface = terminal_intersection, x=0, y=-10, vx=50, vy=0, orientation=0,
                                cartype = Ferrari(),
                                drivertype = SpeedoFerraro())
terminal_intersection.debug_spawn(spawned_vehicle_2)

controller = SimulationController(trafficmap, 200, 100, 60)

controller.run()