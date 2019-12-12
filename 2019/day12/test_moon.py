from moon import Moon

from coordinate import Coordinate


def test_moon_1():
    raw_data = '<x=-2, y=9, z=-5>'
    sut = Moon(raw_data)
    assert sut.p == Coordinate(-2, 9, -5)
    assert sut.v == Coordinate(0, 0, 0)


def test_moon_2():
    raw_data = '<x=16, y=19, z=9>'
    sut = Moon(raw_data)
    assert sut.p == Coordinate(16, 19, 9)
    assert sut.v == Coordinate(0, 0, 0)


def test_moon_3():
    raw_data = '<x=0, y=3, z=6>'
    sut = Moon(raw_data)
    assert sut.p == Coordinate(0, 3, 6)
    assert sut.v == Coordinate(0, 0, 0)


def test_moon_4():
    raw_data = '<x=11, y=0, z=11>'
    sut = Moon(raw_data)
    assert sut.p == Coordinate(11, 0, 11)
    assert sut.v == Coordinate(0, 0, 0)
