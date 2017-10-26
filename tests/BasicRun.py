from SimulationController import SimulationController
from TrafficMap import TrafficMap
from Road import Road

trafficmap = TrafficMap()
trafficmap.roadlist.append(Road([200,200],200, 1, 2, 5.5, 200))
controller = SimulationController(trafficmap, 20, -1, 60)

controller.run()
