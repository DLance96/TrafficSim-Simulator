import pygame

from pygame.locals import *


class DisplayController:

    def __init__(self):
        """
        Initializes DisplayController
        """
        pygame.init()
        self.display_size = 640, 400
        self.display_obj = pygame.display.set_mode(self.display_size, pygame.HWSURFACE | pygame.DOUBLEBUF)

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

