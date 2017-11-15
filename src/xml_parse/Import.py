import math
import sys
import os
import xml.etree.ElementTree as ET

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from src.xml_parse.Exceptions import XMLFormatError
from src.xml_parse.Constants import IMPORT_ROAD_TOLERANCE, LANE_WIDTH
from src.xml_parse.Utils import is_connected_traffic_map, distance, add_angles
from src.Road import Road
from src.Intersection import Intersection


def import_xml(filename):
    roads = []
    intersections = []

    if not os.path.isfile(filename):
        raise FileNotFoundError()
    traffic_map = ET.parse(filename)
    root = traffic_map.getroot()
    for intersection in root.find('intersections'):
        intersections.append(generate_intersection(intersection))
    for road in root.find('roads'):
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
    speed_limit = int(road.find('speed_limit').text)  # TODO: update when speed limit added
    speed_limit = 50 # TODO: testing default
    return_road = Road(anchor_point, length, in_lanes, out_lanes, angle, speed_limit, .01)
    add_connections(return_road, road.find('start_intersection'), road.find('end_intersection'), intersections)

    return return_road


def generate_intersection(intersection):
    if intersection.find('center_point') is None:
        raise XMLFormatError('Missing center point in a intersection')
    coords = intersection.find('center_point').text.split(' ')
    try:
        center_point = [float(coords[0]), float(coords[1])]
    except ValueError:
        raise XMLFormatError('Center coordinates not floats in format \"{float} {float}\"')
    if intersection.find('radius') is None:
        raise XMLFormatError('Missing radius in a intersection')
    radius = float(intersection.find('radius').text)

    return Intersection(center_point, radius, 200)


def validate_geometry(roads, intersections):
    for road in roads:
        start_intersection = road.get_start_connection()
        end_intersection = road.get_end_connection()

        if start_intersection is not None:
            if not math.isclose(distance(road.get_start_coords(), start_intersection.get_center()),
                                start_intersection.get_radius(), IMPORT_ROAD_TOLERANCE):
                raise XMLFormatError('Road start point not on intersection edge')
        if end_intersection is not None:
            if not math.isclose(distance(road.get_end_coords(), end_intersection.get_center()),
                                end_intersection.get_radius(), IMPORT_ROAD_TOLERANCE):
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
    import_xml('temp.xml')
