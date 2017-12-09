from src.SimulationController import SimulationController
from src.TrafficMap import TrafficMap
import pytest

def test_create_SimulationController_zero_fps():
    with pytest.raises(ValueError, match="frame_per_second must be greater than 0"):
        t = TrafficMap(None)
        SimulationController(t, 1,1,0)


def test_create_SimulationController_zero_ticktime_ms():
    with pytest.raises(ValueError, match="ticktime_ms must be greater than 0"):
        t = TrafficMap(None)
        SimulationController(t, 0,1,1)

def test_create_SimulationController_none_map():
    with pytest.raises(ValueError, match="traffic_map cannot be None type"):
        t = TrafficMap(None)
        SimulationController(None, 1,1,1)

