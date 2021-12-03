from day03 import solution


def test_part_1():
    assert solution.part_1("day03/sample") == 198
    assert solution.part_1("day03/input") == 3969000


def test_part_2():
    assert solution.part_2("day03/sample") == 230
    assert solution.part_2("day03/input") == 4267809
