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


