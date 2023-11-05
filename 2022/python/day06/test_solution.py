from day06 import solution


def test_part_1():
    assert solution.part_1("day06/sample") == 7
    assert solution.part_1("day06/input") == 1480


def test_part_2():
    assert solution.part_2("day06/sample") == 19
    assert solution.part_2("day06/input") == 2746
