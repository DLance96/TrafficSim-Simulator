import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.TrafficMap import TrafficMap
from src.SimulationController import SimulationController
from src.xml_parse.Import import import_xml
from src.Reporter import Reporter

def test_import_and_run():
    # First argument is the location of the map .xml file to be simulated
    filename = "tests_gui/temp.xml"
    save_location = "test_out"
    ticktime_ms = 200
    seconds = 60
    frames = 60
    compact = True

    # Create a reporter to handle information collection
    reporter = Reporter()
    # Create a trafficmap to hold the environment objects
    trafficmap = TrafficMap(reporter=reporter)
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

def test_import_run_export():
    # First argument is the location of the map .xml file to be simulated
    filename = "tests_gui/temp.xml"
    save_location = "test_out"
    ticktime_ms = 200
    seconds = 60
    frames = 60
    compact = True

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

def test_import():
    # First argument is the location of the map .xml file to be simulated
    filename = "tests_gui/temp.xml"

    # Create a reporter to handle information collection
    reporter = Reporter()
    # Create a trafficmap to hold the environment objects
    trafficmap = TrafficMap(reporter = reporter)
    # Process the map file to get the list of created roads and intersections
    roads, intersections = import_xml(filename)

    assert len(roads)>0 and len(intersections) > 0 and trafficmap is not None