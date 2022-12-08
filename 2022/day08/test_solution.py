from day08 import solution


def test_part_1():
    assert solution.part_1("day08/sample") == 21
    assert solution.part_1("day08/input") == 1825


def test_part_2():
    assert solution.part_2("day08/sample") == 8
    assert solution.part_2("day08/input") == 235200
