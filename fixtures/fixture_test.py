import math
import pytest

from fixture import Fixture

@pytest.mark.skip(reason="WIP")
def test_density_100pct():
    fix = Fixture(20, 100)
    assert math.isclose(fix.density(), 100)
