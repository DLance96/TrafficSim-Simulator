from SimulationController import SimulationController
from TrafficMap import TrafficMap
from Road import Road
from drivers.DriverTemplate import  DriverTemplate
from vehicles.VehicleTemplate import VehicleTemplate

trafficmap = TrafficMap()
onlyroad = Road([200,200],200, 1, 2, 5.5, 200)
trafficmap.roadlist.append(onlyroad)
controller = SimulationController(trafficmap, 20, -1, 60)
onlyroad.spawn(DriverTemplate(),VehicleTemplate(),0)
controller.run()
