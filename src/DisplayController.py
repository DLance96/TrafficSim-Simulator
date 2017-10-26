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
        move_interval = 1
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
            self.display_zoom = (self.display_zoom[0] + self.display_size[0]/scale_factor),\
                                (self.display_zoom[1] + self.display_size[1]/scale_factor)
            self.xoffset -= self.display_size[0] / scale_factor / 2
            self.yoffset -= self.display_size[1] / scale_factor / 2

        if keys_down[pygame.K_w]:
            if self.display_zoom[0] > 100:
                self.display_zoom = (self.display_zoom[0] - self.display_size[0]/scale_factor),\
                                    (self.display_zoom[1] - self.display_size[1]/scale_factor)

                self.xoffset += self.display_size[0] / scale_factor / 2
                self.yoffset += self.display_size[1] / scale_factor / 2

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

        for road in traffic_map.roadlist:
            self.drawRoad(road)
        temp_surface = pygame.transform.scale(self.draw_surface,tuple(map(int, self.display_zoom)))
        self.display_surface.blit(temp_surface, temp_surface.get_rect().move(self.xoffset, self.yoffset))

        pygame.display.update()

    def drawVehicle(self, road, vehicle):
        """

        :param vehicle:
        :return: None
        """
        first = (vehicle.x, vehicle.y)
        second = (first[0] + vehicle.cartype.length * math.cos(vehicle.orientation),
                  first[1] + vehicle.cartype.length * math.sin(vehicle.orientation))

        third = (second[0] + vehicle.cartype.width * math.cos(vehicle.orientation + math.pi / 2),
                 second[1] + vehicle.cartype.width * math.sin(vehicle.orientation + math.pi / 2))

        fourth = (first[0] + vehicle.cartype.width * math.cos(vehicle.orientation + math.pi / 2),
                  first[1] + vehicle.cartype.width * math.sin(vehicle.orientation + math.pi / 2))

        pointlist = list(map(road.local_to_global_location_conversion, [first, second, third, fourth]))

        vehicle_color = Color(255, 100, 100)

        pygame.draw.polygon(self.draw_surface, vehicle_color, pointlist)

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
        pygame.draw.polygon(self.draw_surface, road_color, pointlist)
        point1 = (first[0] + (fourth[0] - first[0]) * road.inbound_lanes / (road.inbound_lanes + road.outbound_lanes),
                  first[1] + (fourth[1] - first[1]) * road.inbound_lanes / (road.inbound_lanes + road.outbound_lanes))

        point2 = (second[0] + (third[0] - second[0]) * road.inbound_lanes / (road.inbound_lanes + road.outbound_lanes),
                  second[1] + (third[1] - second[1]) * road.inbound_lanes / (road.inbound_lanes + road.outbound_lanes))

        pygame.draw.line(self.draw_surface, Color(250, 210, 1), point1, point2, 3)



