from SimulationController import SimulationController
from TrafficMap import TrafficMap
from Road import Road

trafficmap = TrafficMap()
trafficmap.roadlist.append(Road([0,0],10, 1, 1, 0, 200))
controller = SimulationController(trafficmap, 20, -1, 60)

controller.run()
