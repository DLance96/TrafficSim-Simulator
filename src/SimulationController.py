import pygame
from src.DisplayController import DisplayController
import time
from pygame.locals import *


class SimulationController:
    """
    Handles running the simulation, setting up DisplayController,
    and generating a report in the form of a Reporter object
    Contains a DisplayController and calls render on a specified interval (see: 'frames_per_second')

    :param traffic_map: TrafficMap to be used by the simulation
    :param ticktime_ms: time elapsed by each tick of the simulation
    :param seconds_to_run: number of seconds the simulation should run for. if -1, simulation will run until user termination
    :param frames_per_second: desired frames per second to render the simulation at
    :param display_controller: instance of DisplayController used for rendering
    :type traffic_map: TrafficMap
    :type ticktime_ms: int
    :type steps_to_run: int
    :type frames_per_second: int
    :type display_controller: DisplayController

    """
    def __init__(self, traffic_map, ticktime_ms, seconds_to_run, frames_per_second):
        """
        Inititalizes the SimulationController
        :param traffic_map: TrafficMap to be used by the simulation
        :param ticktime_ms: time elapsed by each tick of the simulation
        :param seconds_to_run: number of seconds the simulation should run for. if -1, simulation will run until user termination
        :param frames_per_second: desired frames per second to render the simulation at
        :type traffic_map: TrafficMap
        :type ticktime_ms: int
        :type steps_to_run: int
        :type frames_per_second: int
        """
        self.traffic_map = traffic_map
        if traffic_map is None:
            raise ValueError("traffic_map cannot be None type")

        self.ticktime_ms = ticktime_ms

        if ticktime_ms <= 0:
            raise ValueError("ticktime_ms must be greater than 0")

        self.seconds_to_run = seconds_to_run

        if frames_per_second <= 0:
            raise ValueError("frame_per_second must be greater than 0")

        self.frames_per_second = frames_per_second

        self.display_controller = DisplayController()

    def run(self):
        """
        Runs the simulation for self.seconds_to_run seconds
        calls render on self.display_controller to draw the simulation
        constructs and returns a Reporter object detailing the simmulation

        :return: Reporter object that contains information of the simulation that ran
        :rtype: Reporter
        """
        seconds_run = 0
        ms_per_frame = 1/self.frames_per_second*1000
        start_time_ms = 0
        while seconds_run < self.seconds_to_run or self.seconds_to_run == -1:
            if self.seconds_to_run != -1:
                seconds_run += float(self.ticktime_ms) / 1000
            self.tick()
            self.tock()
            if start_time_ms + ms_per_frame < int(round(time.time() * 1000)):
                start_time_ms = int(round(time.time() * 1000))
                self.display_controller.render(self.traffic_map)

    def tick(self):
        """
        :return: None
        """
        self.traffic_map.tick(self.ticktime_ms)

    def tock(self):
        """
        :return: None
        """
        self.traffic_map.tock(self.ticktime_ms)
