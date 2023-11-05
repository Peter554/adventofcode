from day01 import solution


def test_part_1():
    assert solution.part_1("day01/sample") == 24000
    assert solution.part_1("day01/input") == 69206


def test_part_2():
    assert solution.part_2("day01/sample") == 45000
    assert solution.part_2("day01/input") == 197400
