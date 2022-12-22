from day22 import solution


def test_parse_route():
    route = solution.parse_route()
    assert route[0] == 15
    assert route[1] == solution.Turn.LEFT
    assert route[2] == 7


def test_parse_maps():
    maps = solution.parse_maps()
    assert set(maps) == {0, 1, 2, 3, 4, 5}
    assert solution.Point2D(0, 0) in maps[0]
    assert solution.Point2D(2, 1) not in maps[0]
    assert solution.Point2D(49, 49) in maps[0]


def test_part_1():
    assert solution.part_1() == 1


def test_part_2():
    assert solution.part_2() == 1
