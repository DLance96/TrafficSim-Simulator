import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.SimulationController import SimulationController
from src.TrafficMap import TrafficMap
from src.Road import Road
from src.Intersection import Intersection
from src.drivers.DriverTemplate import  DriverTemplate
from src.vehicles.VehicleTemplate import VehicleTemplate
from src.TemplatePairFactory import TemplatePairFactory
from src.drivers.DriverTemplate import SpeedoFerraro
from src.drivers.DriverTemplate import SlowDriver
from src.vehicles.VehicleTemplate import Ferrari

trafficmap = TrafficMap()
prebuilt_list = [((0, 1), DriverTemplate(),VehicleTemplate())]
onlyroad = Road([200,200], 800, 2, 2, 0, 50)

initial_intersection = Intersection(center = (100, 220), radius = 130, speed_limit = 50,
                                    template_factory=TemplatePairFactory(10000, prebuilt_list))
terminal_intersection = Intersection(center = (1100, 220), radius = 130, speed_limit = 50,
                                     template_factory=TemplatePairFactory(10000, prebuilt_list))
initial_intersection.bind_road_to_intersection(onlyroad,'terminal')
terminal_intersection.bind_road_to_intersection(onlyroad,'initial')
trafficmap.roadlist.append(onlyroad)
trafficmap.intersectionlist.append(initial_intersection)
trafficmap.intersectionlist.append(terminal_intersection)
controller = SimulationController(trafficmap, 100, 100, 60)

controller.run()
