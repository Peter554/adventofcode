from day09 import solution


def test_part_1():
    assert solution.part_1("day09/sample") == 13
    assert solution.part_1("day09/input") == 6030


def test_part_2():
    assert solution.part_2("day09/sample") == 1
    assert solution.part_2("day09/sample2") == 36
    assert solution.part_2("day09/input") == 2545
