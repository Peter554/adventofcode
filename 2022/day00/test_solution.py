from day00 import solution


def test_part_1():
    with open("day00/input") as f:
        assert solution.part_1(f.readlines()) == 1602


def test_part_2():
    with open("day00/input") as f:
        assert solution.part_2(f.readlines()) == 1633
