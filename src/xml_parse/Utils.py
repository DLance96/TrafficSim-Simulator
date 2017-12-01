import math
from src.xml_parse.Constants import SIG_FIGS


def is_connected_traffic_map(roads, intersections):
    """
    Verifies that a collection of intersections and roads is fully connected
    :param roads: list of roads in the map
    :param intersections: list of intersections in the map
    :return: boolean on whether the map is fully connected
    """
    to_visit_roads = []
    visited_roads = []
    visited_intersections = []

    if len(roads) == 0:
        if len(intersections) == 0 or len(intersections) == 1:
            return True
        else:
            return False

    to_visit_roads.append(roads[0])

    while len(to_visit_roads) > 0:
        road = to_visit_roads.pop()
        visited_roads.append(road)
        new_roads = []
        if road.initial_intersection is not None and road.initial_intersection not in visited_intersections:
            new_roads.extend(road.initial_intersection.adjacent_roads)
            visited_intersections.append(road.initial_intersection)
        if road.terminal_intersection is not None and road.terminal_intersection not in visited_intersections:
            new_roads.extend(road.terminal_intersection.adjacent_roads)
            visited_intersections.append(road.terminal_intersection)
        new_roads = list(set(new_roads))
        remove_visited_roads(new_roads, visited_roads)
        remove_visited_roads(new_roads, to_visit_roads)
        to_visit_roads.extend(new_roads)

    if len(roads) == len(visited_roads) and len(intersections) == len(visited_intersections):
        return True
    else:
        return False


def remove_visited_roads(roads, visited_roads):
    """
    Removes all the previous visted roads from the new roads list
    :param roads: list of new roads to be filtered
    :param visited_roads: list of roads that have already been visited
    :return: removes duplicates between visted roads and roads
    """
    for road in roads:
        if road in visited_roads:
            roads.remove(road)


def add_angles(angle1, angle2):
    return_angle = angle1 + angle2
    if return_angle >= 2 * math.pi:
        return_angle -= 2 * math.pi
    if return_angle < 0:
        return_angle += 2 * math.pi
    return return_angle


def distance(coord1, coord2):
    """
    Gets the distance between the two coords
    :param coord1: xy coordinate
    :param coord2: xy coordinate
    :return: float distance
    """
    x_diff = coord1[0] - coord2[0]
    y_diff = coord1[1] - coord2[1]
    dist = (x_diff ** 2 + y_diff ** 2) ** .5
    return round(dist, SIG_FIGS)
