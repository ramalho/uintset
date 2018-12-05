import math

from fixture import Fixture

def test_density_100pct():
    fix = Fixture(20, 100)
    assert math.isclose(fix.density(), 100)
