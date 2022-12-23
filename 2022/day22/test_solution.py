from day22 import solution


def test_parse_route():
    route = solution.parse_route("day22/input/route")
    assert route[0] == 15
    assert route[1] == solution.Turn.LEFT
    assert route[2] == 7


def test_parse_maps():
    map_size, maps = solution.parse_maps("day22/input/maps")
    assert map_size == 50
    assert set(maps) == {0, 1, 2, 3, 4, 5}
    assert solution.Point2D(0, 0) in maps[0]
    assert solution.Point2D(2, 1) not in maps[0]
    assert solution.Point2D(49, 49) in maps[0]


def test_part_1():
    assert solution.part_1("day22/sample") == 6032
    assert solution.part_1("day22/input") == 50412


def test_part_2():
    assert solution.part_2("day22/input") == 130068
