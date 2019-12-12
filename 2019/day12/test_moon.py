from moon import Moon


def test_moon_1():
    raw_data = '<x=-2, y=9, z=-5>'
    sut = Moon(raw_data)
    assert sut.p.x == -2
    assert sut.p.y == 9
    assert sut.p.z == -5


def test_moon_2():
    raw_data = '<x=16, y=19, z=9>'
    sut = Moon(raw_data)
    assert sut.p.x == 16
    assert sut.p.y == 19
    assert sut.p.z == 9
