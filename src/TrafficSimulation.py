import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.TrafficMap import TrafficMap
from src.SimulationController import SimulationController
from src.xml_parse.Import import import_xml
from src.Reporter import Reporter

if __name__ == '__main__':

    filename = sys.argv[1]
    save_location = sys.argv[2]
    ticktime_ms = int(sys.argv[3])
    seconds = int(sys.argv[4])
    frames = int(sys.argv[5])
    compact = True if sys.argv[6] == "compact" else False

    reporter = Reporter()

    trafficmap = TrafficMap(reporter = reporter)

    roads, intersections = import_xml(filename)

    for road in roads:
        trafficmap.add_road(road)
    for intersection in intersections:
        trafficmap.add_intersection(intersection)

    controller = SimulationController(trafficmap, ticktime_ms, seconds, frames)

    controller.run()

    if compact:
        reporter.generate_compact_report(save_location)
    else:
        reporter.generate_complete_report(save_location)
