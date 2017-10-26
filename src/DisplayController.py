import pygame

from pygame.locals import *


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

        for road in traffic_map.roadlist:
            self.drawRoad(road)

    def drawRoad(self, road):
        """
        :param road: Instance of a Road to get rectangle of
        :type road: Road
        :return: None
        """
        rectangle_to_draw = Rect(road.anchor[0], road.anchor[1], road.length,
                                 road.lane_width*road.outbound_lanes+road.lane_width*road.inbound_lanes)
        pygame.draw.rect(self.display_surface, rectangle_to_draw, Color(200,200,200))


