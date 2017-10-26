import pygame
import math
from pygame.locals import *
from Road import Road

class DisplayController:

    def __init__(self):
        """
        Initializes DisplayController
        """
        pygame.init()
        self.display_size = 640, 400
        self.display_surface = pygame.display.set_mode(self.display_size, pygame.HWSURFACE | pygame.DOUBLEBUF)

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

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pygame.quit()
            quit()

        self.display_surface.fill(Color(255,255,255))

        for road in traffic_map.roadlist:
            self.drawRoad(road)

        pygame.display.update()

    def drawVehicle(self, vehicle):
        """

        :param vehicle:
        :return:
        """

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

        pointlist = [first,second,third,fourth]
        road_color = Color(100,100,100)
        pygame.draw.polygon(self.display_surface, road_color, pointlist)
        point1 = (first[0] + (fourth[0] - first[0]) * road.inbound_lanes / (road.inbound_lanes + road.outbound_lanes),
                  first[1] + (fourth[1] - first[1]) * road.inbound_lanes / (road.inbound_lanes + road.outbound_lanes))

        point2 = (second[0] + (third[0] - second[0]) * road.inbound_lanes / (road.inbound_lanes + road.outbound_lanes),
                  second[1] + (third[1] - second[1]) * road.inbound_lanes / (road.inbound_lanes + road.outbound_lanes))

        pygame.draw.line(self.display_surface, Color(250, 210, 1), point1, point2, 3)



