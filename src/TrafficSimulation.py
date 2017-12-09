import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.TrafficMap import TrafficMap
from src.SimulationController import SimulationController
from src.xml_parse.Import import import_xml
from src.Reporter import Reporter

# Script for running the simulation
if __name__ == '__main__':

    # First argument is the location of the map .xml file to be simulated
    filename = sys.argv[1]
    # Second argument is the location to save the report
    save_location = sys.argv[2]
    # third argument is the length in ms of the simulation tick
    ticktime_ms = int(sys.argv[3])
    # fourth argument is the number of seconds to simulate
    seconds = int(sys.argv[4])
    # fifth argument is the maximum number of FPS to display, if possible
    frames = int(sys.argv[5])
    # sixth argument is whether or not to produce a compact report (see Report.py)
    compact = True if sys.argv[6] == "compact" else False

    # Create a reporter to handle information collection
    reporter = Reporter()
    # Create a trafficmap to hold the environment objects
    trafficmap = TrafficMap(reporter = reporter)
    # Process the map file to get the list of created roads and intersections
    roads, intersections = import_xml(filename)

    # Add each of the environment objects (Road/Intersection) to the trafficmap
    for road in roads:
        trafficmap.add_road(road)
    for intersection in intersections:
        trafficmap.add_intersection(intersection)

    # Create a simulation controller with the relevant information
    controller = SimulationController(trafficmap, ticktime_ms, seconds, frames)

    # Run the simulation
    controller.run()

    # Write out the report
    if compact:
        reporter.generate_compact_report(save_location)
    else:
        reporter.generate_complete_report(save_location)
