from day14 import solution


def test_part_1():
    assert solution.part_1("day14/sample") == 24
    assert solution.part_1("day14/input") == 1298


def test_part_2():
    assert solution.part_2("day14/sample") == 93
    assert solution.part_2("day14/input") == 25585
