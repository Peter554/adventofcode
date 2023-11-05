from day04 import solution


def test_part_1():
    assert solution.part_1("day04/sample") == 2
    assert solution.part_1("day04/input") == 450


def test_part_2():
    assert solution.part_2("day04/sample") == 4
    assert solution.part_2("day04/input") == 837
