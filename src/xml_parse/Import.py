import math
import sys
import os
import xml.etree.ElementTree as ET

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from src.xml_parse.Exceptions import XMLFormatError
from src.xml_parse.Constants import IMPORT_ROAD_TOLERANCE, LANE_WIDTH, TEMPLATE_PAIR_FREQ_DEFAULT
from src.xml_parse.Utils import is_connected_traffic_map, distance, add_angles
from src.TemplatePairFactory import TemplatePairFactory
from src.drivers.DriverTemplate import DriverTemplate
from src.vehicles.VehicleTemplate import VehicleTemplate
from src.Road import Road
from src.Intersection import Intersection
from src.TrafficMap import TrafficMap
from src.SimulationController import SimulationController


def import_xml(filename):
    roads = []
    intersections = []

    if not os.path.isfile(filename):
        raise FileNotFoundError()
    traffic_map = ET.parse(filename)
    root = traffic_map.getroot()
    xml_intersections = root.findall('intersection')
    xml_roads = root.findall('road')
    for intersection in xml_intersections:
        intersections.append(generate_intersection(intersection))
    for road in xml_roads:
        roads.append(generate_road(road, intersections))

    if not is_connected_traffic_map(roads, intersections):
        raise XMLFormatError('Traffic Map is not connected')
    validate_geometry(roads, intersections)

    return roads, intersections


def generate_road(road, intersections):
    if road.find('length') is None:
        raise XMLFormatError('Missing length in a road')
    length = float(road.find('length').text)
    if road.find('incoming_lanes') is None:
        raise XMLFormatError('Missing incoming lanes count in road')
    in_lanes = int(road.find('incoming_lanes').text)
    if road.find('outgoing_lanes') is None:
        raise XMLFormatError('Missing outgoing lanes count in road')
    out_lanes = int(road.find('outgoing_lanes').text)
    if road.find('angle_radians') is None:
        raise XMLFormatError('Missing angle in road')
    angle = float(road.find('angle_radians').text)
    if road.find('anchor_point') is None:
        raise XMLFormatError('Missing anchor point in road')
    coords = road.find('anchor_point').text.split(' ')
    try:
        anchor_point = [float(coords[0]), float(coords[1])]
    except ValueError:
        raise XMLFormatError('Anchor coordinates not floats in format \"{float} {float}\"')
    if road.find('speed_limit') is None:
        raise XMLFormatError('Missing speed limit in road')
    speed_limit = int(road.find('speed_limit').text)
    return_road = Road(anchor_point, length, in_lanes, out_lanes, angle, speed_limit)
    add_connections(return_road, road.find('start_intersection'), road.find('end_intersection'), intersections)

    return return_road


def generate_intersection(intersection):
    template_pair_factory = None
    traffic_cycle = None

    if intersection.find('center_point') is None:
        raise XMLFormatError('Missing center point in a intersection')
    coords = intersection.find('center_point').text.split(' ')
    try:
        center_point = [float(coords[0]), float(coords[1])]
    except ValueError:
        raise XMLFormatError('Center coordinates not floats in format \"{float} {float}\"')
    if intersection.find('radius') is None:
        raise XMLFormatError('Missing radius in a intersection')
    radius = int(intersection.find('radius').text)
    if intersection.find('driver_vehicle_template') is None:
        template_pair_factory = TemplatePairFactory(TEMPLATE_PAIR_FREQ_DEFAULT,
                                                    [((0, 1), DriverTemplate(),VehicleTemplate())])
    if intersection.find('traffic_cycle') is not None:
        pass

    return Intersection(center=center_point, radius=radius, speed_limit=200,
                        template_factory=template_pair_factory, traffic_cycle=traffic_cycle)


def validate_geometry(roads, intersections):
    for road in roads:
        start_intersection = road.initial_intersection
        end_intersection = road.terminal_intersection

        if start_intersection is not None:
            if not math.isclose(distance(road.anchor, start_intersection.center),
                                start_intersection.radius, rel_tol=IMPORT_ROAD_TOLERANCE):
                raise XMLFormatError('Road start point not on intersection edge')
        if end_intersection is not None:
            end_anchor = [road.anchor[0] + road.length * math.cos(road.orientation),
                          road.anchor[1] + road.length * math.sin(road.orientation)]
            if not math.isclose(distance(end_anchor, end_intersection.center),
                                end_intersection.radius, rel_tol=IMPORT_ROAD_TOLERANCE):
                raise XMLFormatError('Road end point not on intersection edge')
                # TODO: add overloaded intersections
    return True


def add_connections(road, start, end, intersections):
    if start is not None:
        if not 0 <= int(start.text) < len(intersections):
            raise XMLFormatError('Start intersection does not exist')
        intersections[int(start.text)].bind_road_to_intersection(road, "initial")
    if end is not None:
        if not 0 <= int(end.text) < len(intersections):
            raise XMLFormatError('End intersection does not exist')
        intersections[int(end.text)].bind_road_to_intersection(road, "terminal")


def get_chord_center(angle_of_perpendicular, chord_length, anchor_point):
    angle = add_angles(angle_of_perpendicular, math.pi / 2)
    return [anchor_point[0] + math.cos(angle) * chord_length / 2,
            anchor_point[1] + math.sin(angle) * chord_length / 2]


def in_intersection(intersection, point):
    return True if distance(intersection.get_center(), point) < intersection.get_radius() else False


if __name__ == '__main__':
    roads, intersections = import_xml('/home/david/Documents/Class/EECS393/TrafficSim-Simulator/temp.xml')
    trafficmap = TrafficMap()

    for road in roads:
        trafficmap.roadlist.append(road)
    for intersection in intersections:
        trafficmap.intersectionlist.append(intersection)

    controller = SimulationController(trafficmap, 200, 100, 60)

    controller.run()