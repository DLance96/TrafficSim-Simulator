import time
import operator
import random
import math
from src.vehicles.VehicleTemplate import VehicleTemplate
from src.drivers.DriverTemplate import DriverTemplate


class Reporter:
    class Report:

        def __init__(self):
            self.number_of_vehicles_list = []
            self.average_speed_list = []
            self.number_of_crashes_list = []

        def add(self, number_of_vehicles, average_speed, number_of_crashes):
            self.number_of_vehicles_list.append(number_of_vehicles)
            self.average_speed_list.append(average_speed)
            self.number_of_crashes_list.append(number_of_crashes)
            return

        def read(self):
            return self.number_of_vehicles_list, self.average_speed_list, self.number_of_crashes_list

    def __init__(self):

        self.intersection_report_table = {}
        self.road_report_table = {}

    def create_intersection_entry(self, intersection_name):
        self.intersection_report_table[intersection_name] = self.Report()

    def create_road_entry(self, road_name):
        self.road_report_table[road_name] = self.Report()

    def add_info_intersection(self, name, number_of_vehicles, average_speed, number_of_crashes):
        self.intersection_report_table[name].add(number_of_vehicles, average_speed, number_of_crashes)

    def add_info_road(self, name, number_of_vehicles, average_speed, number_of_crashes):
        self.road_report_table[name].add(number_of_vehicles, average_speed, number_of_crashes)

    def generate_complete_report(self, output_file = None):

        if output_file is None:
            output = "Default_Report_Name"
        else:
            output = output_file

        with open(output + '.txt', "w+") as f:
            f.write("Traffic System Report\n")
            f.write("Intersections\n")
            for name, report in self.intersection_report_table.items():
                f.write("" + name + "\n")
                vehicle_numbers, avg_speed_numbers, crash_numbers = report.read()
                f.write("Number of Vehicles in the Intersection\n")
                f.write(str(vehicle_numbers) + '\n')
                f.write("Average Speed of Vehicles in the Intersection\n")
                f.write(str(avg_speed_numbers) + '\n')
                f.write("Number of Crashes in the Intersection\n")
                f.write(str(crash_numbers) + '\n')
            f.write("Roads\n")
            for name, report in self.road_report_table.items():
                f.write("" + name + "\n")
                vehicle_numbers, avg_speed_numbers, crash_numbers = report.read()
                f.write("Number of Vehicles on the Road\n")
                f.write(str(vehicle_numbers) + '\n')
                f.write("Average Speed of Vehicles on the Road\n")
                f.write(str(avg_speed_numbers) + '\n')
                f.write("Number of Crashes on the Road\n")
                f.write(str(crash_numbers) + '\n')
        return

    def generate_compact_report(self, output_file = None):

        if output_file is None:
            output = "Default_Report_Name"
        else:
            output = output_file

        with open(output + '.txt', "w+") as f:
            f.write("Traffic System Report\n")
            f.write("Intersections\n")
            print(len(self.intersection_report_table.items()))
            for name, report in self.intersection_report_table.items():
                f.write(str(name) + "\n")
                vehicle_numbers, avg_speed_numbers, crash_numbers = report.read()
                avg_speed_numbers = list(filter(lambda x: not x == "NAN", avg_speed_numbers))
                f.write("Average Number of Vehicles in the Intersection\n")
                f.write(str(sum(vehicle_numbers)/len(vehicle_numbers)) + '\n')
                f.write("Average Average Speed of Vehicles in the Intersection\n")
                f.write(str(sum(avg_speed_numbers)/len(avg_speed_numbers)) + '\n')
                f.write("Average Number of Crashes in the Intersection\n")
                f.write(str(sum(crash_numbers)) + '\n')
            f.write("Roads\n")
            print(len(self.road_report_table.items()))
            for name, report in self.road_report_table.items():
                f.write(str(name) + "\n")
                vehicle_numbers, avg_speed_numbers, crash_numbers = report.read()
                avg_speed_numbers = list(filter(lambda x: not x == "NAN", avg_speed_numbers))
                f.write("Average Number of Vehicles on the Road\n")
                f.write(str(sum(vehicle_numbers)/len(vehicle_numbers)) + '\n')
                f.write("Average - Average Speed of Vehicles on the Road\n")
                f.write(str(sum(avg_speed_numbers)/len(avg_speed_numbers)) + '\n')
                f.write("Average Number of Crashes on the Road\n")
                f.write(str(sum(crash_numbers)) + '\n')
        return
