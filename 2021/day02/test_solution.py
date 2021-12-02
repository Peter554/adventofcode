from day02 import solution


def test_part_1():
    assert solution.part_1("day02/sample") == 150
    assert solution.part_1("day02/input") == 1692075


def test_part_2():
    assert solution.part_2("day02/sample") == 900
    assert solution.part_2("day02/input") == 1749524700
