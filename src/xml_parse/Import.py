import math
import sys
import os
import xml.etree.ElementTree as ET
from pygame.locals import Color

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from src.xml_parse.Exceptions import XMLFormatError
from src.xml_parse.Constants import IMPORT_ROAD_TOLERANCE, LANE_WIDTH, TEMPLATE_PAIR_FREQ_DEFAULT, YELLOW_DEFAULT
from src.xml_parse.Utils import is_connected_traffic_map, distance, add_angles
from src.TemplatePairFactory import TemplatePairFactory
from src.drivers.DriverTemplate import DriverTemplate
from src.vehicles.VehicleTemplate import VehicleTemplate
from src.Road import Road
from src.Intersection import Intersection
from src.TrafficMap import TrafficMap
from src.TrafficCycle import TrafficCycle
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
    if intersection.find('spawning_profiles') is None:
        pass
        template_pair_factory = TemplatePairFactory(TEMPLATE_PAIR_FREQ_DEFAULT,
                                                    [((0, 1), DriverTemplate(), VehicleTemplate())])
    else:
        spawning_profiles = []
        frequency = int(intersection.find('spawning_profiles').text)
        for spawning_profile in intersection.find('spawning_profiles').findall('profile'):
            driver_profile = spawning_profile.find('driver')
            vehicle_profile = spawning_profile.find('vehicle')

            brake_factor = float(driver_profile.find('brake_factor').text)
            speed_offset = int(driver_profile.find('speed_offset').text)
            follow_time = int(driver_profile.find('follow_time').text)
            driver_max_accel = int(driver_profile.find('max_accel').text)
            driver_min_accel = int(driver_profile.find('min_accel').text)
            max_speed = int(driver_profile.find('max_speed').text)
            accel_time = int(driver_profile.find('accel_time').text)
            update_time = int(driver_profile.find('update_time').text)
            inter_time = int(driver_profile.find('inter_time').text)
            driver_color_values = list(map(int, driver_profile.find('color').split(' ')))
            driver_color = Color(driver_color_values[0], driver_color_values[1], driver_color_values[2])

            driver = DriverTemplate(brake_factor, speed_offset, follow_time, driver_max_accel, driver_min_accel,
                                    max_speed, accel_time, update_time, inter_time, driver_color)

            length = int(vehicle_profile.find('length').text)
            width = int(vehicle_profile.find('width').text)
            vehicle_max_decel = float(vehicle_profile.find('max_decel').text)
            vehicle_max_accel = float(vehicle_profile.find('max_accel').text)
            mass = int(vehicle_profile.find('mass').text)
            max_speed = int(vehicle_profile.find('max_speed').text)
            turn_speed = int(vehicle_profile.find('turn_speed').text)
            vehicle_color_values = list(map(int, vehicle_profile.find('color').split(' ')))
            vehicle_color = Color(vehicle_color_values[0], vehicle_color_values[1], vehicle_color_values[2])

            vehicle = VehicleTemplate(length, width, vehicle_max_decel, vehicle_max_accel,
                                      mass, max_speed, turn_speed, vehicle_color)

            probability_range = list()
            starting_prob = len(spawning_profiles) / len(intersection.find('spawning_profiles').findall('profile'))
            ending_prob = (1 + len(spawning_profiles)) / len(intersection.find('spawning_profiles').findall('profile'))
            probability_range.append(starting_prob)
            probability_range.append(ending_prob)

            profile = (probability_range, driver, vehicle)
            spawning_profiles.append(profile)
        template_pair_factory = TemplatePairFactory(frequency, spawning_profiles, mix_and_match=False)

    if intersection.find('traffic_cycle') is not None:
        green_light = []
        timings = []
        if intersection.find('traffic_cycle').find('yellow_light') is not None:
            yellow_light = 1000 * int(intersection.find('traffic_cycle').find('yellow_light').text)
        else:
            yellow_light = YELLOW_DEFAULT
        for cycle in intersection.find('traffic_cycle').findall('cycle'):
            green_light.append(list(map(int, cycle.find('roads').text.split(' '))))
            timings.append(int(cycle.find('timing').text))
        traffic_cycle = TrafficCycle(green_lights=green_light, timings=timings, yellow_light_length=yellow_light)

    return Intersection(center=center_point, radius=radius, speed_limit=200,
                        template_factory=template_pair_factory, traffic_cycle=traffic_cycle)


def validate_geometry(roads, intersections):
    # To be removed
    return True
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