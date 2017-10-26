from src.Road import Road
from src.Intersection import Intersection

def init_intersection(center, radius, speed_limit):
    intersection = Intersection(center=center, radius=radius, speed_limit=speed_limit)
    out1 = intersection.center
    out2 = intersection.radius
    out3 = intersection.speed_limit
    return (out1, out2, out3)

def test_init_intersection():
    assert init_intersection((100, 200), 300, 400) == ((100, 200), 300, 400)
