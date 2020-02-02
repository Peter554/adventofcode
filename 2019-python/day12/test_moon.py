import pytest

from coordinate import Coordinate
from moon import Moon


@pytest.mark.parametrize('x,y,z', [
    (-2, 9, -5),
    (16, 19, 6),
    (0, 3, 6),
    (11, 0, 11)
])
def test_moon_init(x, y, z):
    raw_data = f'<x={x}, y={y}, z={z}>'
    sut = Moon(raw_data)
    assert sut.p == Coordinate(x, y, z)
    assert sut.v == Coordinate(0, 0, 0)
