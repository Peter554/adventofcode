import functools

from app import find_best_location, are_same_direction, compare_func, get_angle


def test_are_equal_1():
    assert are_same_direction((0, 0), (0, 0))
    assert are_same_direction((1, 1), (1, 1))
    assert are_same_direction((-1, -1), (-1, -1))
    assert are_same_direction((3, 7), (9, 21))
    assert are_same_direction((10000001, 1), (10000001, 1))
    assert are_same_direction((-2, 0), (-10, 0))
    assert are_same_direction((0, 1), (0, 3))


def test_are_equal_2():
    assert not are_same_direction((0, 1), (0, 0))
    assert not are_same_direction((1, 0), (0, 0))
    assert not are_same_direction((0, 0), (1, 0))
    assert not are_same_direction((0, 0), (0, 1))
    assert not are_same_direction((1, 1), (-1, -1))
    assert not are_same_direction((10000001, 1), (10000002, 1))


def test_example_1():
    raw_data = [
        "......#.#.",
        "#..#.#....",
        "..#######.",
        ".#.#.###..",
        ".#..#.....",
        "..#....#.#",
        "#..#....#.",
        ".##.#..###",
        "##...#..#.",
        ".#....####",
    ]
    best_location, best_count = find_best_location(raw_data)
    assert best_location == (5, 8)
    assert best_count == 33


def test_example_2():
    raw_data = [
        "#.#...#.#.",
        ".###....#.",
        ".#....#...",
        "##.#.#.#.#",
        "....#.#.#.",
        ".##..###.#",
        "..#...##..",
        "..##....##",
        "......#...",
        ".####.###.",
    ]
    best_location, best_count = find_best_location(raw_data)
    assert best_location == (1, 2)
    assert best_count == 35


def test_example_3():
    raw_data = [
        ".#..#..###",
        "####.###.#",
        "....###.#.",
        "..###.##.#",
        "##.##.#.#.",
        "....###..#",
        "..#.#..#.#",
        "#..#.#.###",
        ".##...##.#",
        ".....#.#..",
    ]
    best_location, best_count = find_best_location(raw_data)
    assert best_location == (6, 3)
    assert best_count == 41


def test_get_angle_1():
    angle_1 = get_angle((0, -1))
    angle_2 = get_angle((1, 0))
    angle_3 = get_angle((0, 1))
    angle_4 = get_angle((-1, 0))
    assert round(angle_1, 2) == 0.00
    assert round(angle_2, 2) == 1.57
    assert round(angle_3, 2) == 3.14
    assert round(angle_4, 2) == 4.71


def test_compare_func_1():
    targets = [
        (-1, -1),
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -2),
        (2, 0),
        (0, 2),
        (0, -1),
        (1, -1),
        (-1, 1),
    ]

    targets.sort(key=functools.cmp_to_key(compare_func))
    assert targets[0] == (0, -1)
    assert targets[1] == (0, -2)
    assert targets[2] == (1, -1)
    assert targets[3] == (1, 0)
    assert targets[4] == (2, 0)
    assert targets[5] == (0, 1)
    assert targets[6] == (0, 2)
    assert targets[7] == (-1, 1)
    assert targets[8] == (-1, 0)
    assert targets[9] == (-1, -1)
