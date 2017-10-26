from src.SimulationController import SimulationController
from src.TrafficMap import TrafficMap
from src.Road import Road
from src.Intersection import Intersection
from src.drivers.DriverTemplate import  DriverTemplate
from src.vehicles.VehicleTemplate import VehicleTemplate
import pytest


def init_intersection(anchor, length, inbound_lanes, outbound_lanes, orientation, speed_limit):
    road = Road(anchor, length, inbound_lanes, outbound_lanes, orientation, speed_limit)
    out1 = road.anchor
    out2 = road.length
    out3 = road.inbound_lanes
    out4 = road.outbound_lanes
    out5 = road.orientation
    out6 = road.speed_limit
    return (out1, out2, out3, out4, out5, out6)


def test_init_intersection():
    assert init_intersection((1, 2), 3, 4, 5, 6, 7) == ((1, 2), 3, 4, 5, 6, 7)


def add_intersections_to_road(speed_limit_1, speed_limit_2):
    road = Road([200, 200], 200, 2, 2, 0, 200)
    initial_intersection = Intersection(center=(200, 220), radius=30, speed_limit=speed_limit_1)
    terminal_intersection = Intersection(center=(400, 220), radius=30, speed_limit=speed_limit_2)
    road.add_neighboring_intersection(initial_intersection, 'initial')
    road.add_neighboring_intersection(terminal_intersection, 'terminal')
    out1 = road.initial_intersection.speed_limit
    out2 = road.terminal_intersection.speed_limit
    return (out1, out2)


def test_add_intersections_to_road():
    assert add_intersections_to_road(100, 200) == (100, 200)


def test_road_handoff():
    """
    Tests to see if road raises an exception upon passing a vehicle to nothing
    :return: None
    """
    trafficmap = TrafficMap()
    onlyroad = Road([200, 200], 300, 2, 2, 0, 200)
    initial_intersection = Intersection(center=(200, 220), radius=30, speed_limit=200)
    onlyroad.add_neighboring_intersection(initial_intersection, 'initial')
    trafficmap.roadlist.append(onlyroad)
    trafficmap.intersectionlist.append(initial_intersection)
    controller = SimulationController(trafficmap, 20, 10, 60)
    onlyroad.spawn(VehicleTemplate(), DriverTemplate(), 0)
    with pytest.raises(Exception) as einfo:
        controller.run()

def test_road_drive_over():
    """
    Roads crossing over other roads should not influence car driving behavior
    ei: like a highway bridge crossing a local road
    :return: None
    """
    trafficmap = TrafficMap()
    road1 = Road([200, 200], 200, 2, 2, 0, 200)
    initial_intersection = Intersection(center=(200, 220), radius=30, speed_limit=200)
    terminal_intersection = Intersection(center=(400, 220), radius=30, speed_limit=200)
    road1.add_neighboring_intersection(initial_intersection, 'initial')
    road1.add_neighboring_intersection(terminal_intersection, 'terminal')
    road2 = Road([300, 300], 200, 2, 2, 4.7, 200)
    trafficmap.roadlist.append(road2)
    trafficmap.roadlist.append(road1)
    trafficmap.intersectionlist.append(initial_intersection)
    trafficmap.intersectionlist.append(terminal_intersection)
    controller = SimulationController(trafficmap, 20, 10, 60)
    road1.spawn(VehicleTemplate(), DriverTemplate(), 0)
    try:
        controller.run()
    except:
        pytest.fail("Raised exception when roads cross roads")

def test_intersection_drive_over():
    trafficmap = TrafficMap()
    onlyroad = Road([200, 200], 200, 2, 2, 0, 200)
    initial_intersection = Intersection(center=(200, 220), radius=30, speed_limit=200)
    terminal_intersection = Intersection(center=(400, 220), radius=30, speed_limit=200)
    onlyroad.add_neighboring_intersection(initial_intersection, 'initial')
    onlyroad.add_neighboring_intersection(terminal_intersection, 'terminal')
    trafficmap.roadlist.append(onlyroad)
    middle_intersection = Intersection(center=(300, 220), radius=40, speed_limit=200)
    trafficmap.intersectionlist.append(middle_intersection)
    trafficmap.intersectionlist.append(initial_intersection)
    trafficmap.intersectionlist.append(terminal_intersection)
    controller = SimulationController(trafficmap, 20, 10, 60)
    onlyroad.spawn(VehicleTemplate(), DriverTemplate(), 0)
    try:
        controller.run()
    except:
        pytest.fail("Raised exception when roads cross intersections")
