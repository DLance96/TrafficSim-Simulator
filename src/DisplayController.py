import pygame
import math
import random
from pygame.locals import *
from src.Road import Road


class DisplayController:
    def __init__(self):
        """
        Initializes DisplayController
        """
        pygame.init()
        self.display_size = 1200, 800
        self.display_surface = pygame.display.set_mode(self.display_size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.draw_surface = pygame.Surface(self.display_size)

        self.xoffset = 0
        self.yoffset = 0
        self.display_zoom = self.display_size

    def transform(self, keys_down):
        """
        :param keys_down: boolean array of keys currently pressed
        :type keys_down: list(bool)
        :return: None
        """
        move_interval = int(10 * self.display_size[0] / self.display_zoom[0])
        scale_factor = 100
        if keys_down[pygame.K_LEFT]:
            self.xoffset += move_interval

        if keys_down[pygame.K_RIGHT]:
            self.xoffset -= move_interval

        if keys_down[pygame.K_UP]:
            self.yoffset += move_interval

        if keys_down[pygame.K_DOWN]:
            self.yoffset -= move_interval

        if keys_down[pygame.K_q]:
            self.display_zoom = (self.display_zoom[0] * 1.01), \
                                (self.display_zoom[1] * 1.01)
            # self.xoffset -= self.display_size[0] / scale_factor / 2
            # self.yoffset -= self.display_size[1] / scale_factor / 2

        if keys_down[pygame.K_w]:
            if self.display_zoom[0] > 100:
                self.display_zoom = (self.display_zoom[0] / 1.01), \
                                    (self.display_zoom[1] / 1.01)

                # self.xoffset += self.display_size[0] / scale_factor / 2
                # self.yoffset += self.display_size[1] / scale_factor / 2

    def render(self, traffic_map):
        """
        :param traffic_map: traffic map to be rendered
        :type traffic_map: TrafficMap
        :rtype: None
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys_down = pygame.key.get_pressed()

        if keys_down[pygame.K_ESCAPE]:
            pygame.quit()
            quit()

        self.transform(keys_down)

        self.draw_surface.fill(Color(255, 255, 255))

        for intersection in traffic_map.get_intersections():
            self.drawIntersection(intersection)
        for road in traffic_map.get_roads():
            self.drawRoad(road)

        for intersection in traffic_map.get_intersections():
            for vehicle in intersection.vehicles:
                self.drawVehicle(intersection, vehicle)

        for road in traffic_map.get_roads():
            for vehicle in road.vehicles:
                self.drawVehicle(road, vehicle)

        for intersection in traffic_map.get_intersections():
            for angle in intersection.adjacent_road_orientations:
                pygame.draw.circle(self.draw_surface, Color(255, 120, 70),
                                   (int(intersection.center[0] + math.cos(angle) * intersection.radius),
                                    int(intersection.center[1] + math.sin(angle) * intersection.radius)), 4)
        for intersection in traffic_map.get_intersections():
            for value, angle in enumerate(intersection.adjacent_road_bounding_orientations):
                pygame.draw.circle(self.draw_surface, Color(value*100, 250-value*120, 250-value*70),
                                   (int(intersection.center[0] + math.cos(angle[0]) * intersection.radius),
                                    int(intersection.center[1] + math.sin(angle[0]) * intersection.radius)), 4)
                pygame.draw.circle(self.draw_surface, Color(value * 100, 250 - value * 120, 250 - value * 70),
                                   (int(intersection.center[0] + math.cos(angle[1]) * intersection.radius),
                                    int(intersection.center[1] + math.sin(angle[1]) * intersection.radius)), 4)

        temp_surface = pygame.transform.scale(self.draw_surface, tuple(map(int, self.display_zoom)))
        self.display_surface.blit(temp_surface, temp_surface.get_rect().move(self.xoffset, self.yoffset))

        pygame.display.update()

    def drawVehicle(self, container, vehicle):
        """
        :param vehicle:
        :return: None
        """

        pointlist = list(map(container.local_to_global_location_conversion, vehicle.get_bounding_points()))

        avgx = 0
        avgy = 0
        for point in pointlist:
            avgx += point[0] / len(pointlist)
            avgy += point[1] / len(pointlist)

        pygame.draw.polygon(self.draw_surface, vehicle.cartype.color, pointlist)
        pygame.draw.circle(self.draw_surface, vehicle.drivertype.color, (int(avgx), int(avgy)),
                           int(vehicle.cartype.width / 2))

    def drawRoad(self, road):
        """
        :param road: Instance of a Road to get rectangle of
        :type road: Road
        :return: None
        """
        first = road.anchor
        second = (first[0] + road.length * math.cos(road.orientation),
                  first[1] + road.length * math.sin(road.orientation))

        third = (second[0] + road.width * math.cos(road.orientation + math.pi / 2),
                 second[1] + road.width * math.sin(road.orientation + math.pi / 2))

        fourth = (first[0] + road.width * math.cos(road.orientation + math.pi / 2),
                  first[1] + road.width * math.sin(road.orientation + math.pi / 2))

        pointlist = [first, second, third, fourth]
        road_color = Color(100, 100, 100)
        pygame.draw.polygon(self.draw_surface, road_color, pointlist)
        point1 = (first[0] + (fourth[0] - first[0]) * road.inbound_lanes / (road.inbound_lanes + road.outbound_lanes),
                  first[1] + (fourth[1] - first[1]) * road.inbound_lanes / (road.inbound_lanes + road.outbound_lanes))

        point2 = (second[0] + (third[0] - second[0]) * road.inbound_lanes / (road.inbound_lanes + road.outbound_lanes),
                  second[1] + (third[1] - second[1]) * road.inbound_lanes / (road.inbound_lanes + road.outbound_lanes))

        pygame.draw.line(self.draw_surface, Color(250, 210, 1), point1, point2, 3)

    def drawIntersection(self, intersection):
        """
        :param intersection: instance of intersection to draw
        :type intersection: Intersection
        :return:
        """
        road_color = Color(100, 100, 100)
        pygame.draw.circle(self.draw_surface, road_color, intersection.center, intersection.radius)
