from src.Vehicle import Vehicle
from src.Road import Road
from src.Bucket import Bucket
import pytest

def test_invalid_construction():
    with pytest.raises(ValueError, match="Vehicle constructor requires a Road or an Intersection."):
        v = Vehicle(None)