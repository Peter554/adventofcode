from app import find_best_location, are_same_direction


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
        '......#.#.',
        '#..#.#....',
        '..#######.',
        '.#.#.###..',
        '.#..#.....',
        '..#....#.#',
        '#..#....#.',
        '.##.#..###',
        '##...#..#.',
        '.#....####'
    ]
    best_location, best_count = find_best_location(raw_data)
    assert best_location == (5, 8)
    assert best_count == 33


def test_example_2():
    raw_data = [
        '#.#...#.#.',
        '.###....#.',
        '.#....#...',
        '##.#.#.#.#',
        '....#.#.#.',
        '.##..###.#',
        '..#...##..',
        '..##....##',
        '......#...',
        '.####.###.'
    ]
    best_location, best_count = find_best_location(raw_data)
    assert best_location == (1, 2)
    assert best_count == 35


def test_example_3():
    raw_data = [
        '.#..#..###',
        '####.###.#',
        '....###.#.',
        '..###.##.#',
        '##.##.#.#.',
        '....###..#',
        '..#.#..#.#',
        '#..#.#.###',
        '.##...##.#',
        '.....#.#..'
    ]
    best_location, best_count = find_best_location(raw_data)
    assert best_location == (6, 3)
    assert best_count == 41
