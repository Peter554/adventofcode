from day13 import solution


def test_part_1():
    assert solution.part_1("day13/sample") == 13
    assert solution.part_1("day13/input") == 5825


def test_part_2():
    assert solution.part_2("day13/sample") == 140
    assert solution.part_2("day13/input") == 24477
