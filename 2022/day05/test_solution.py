from day05 import solution


def test_part_1():
    assert solution.part_1("day05/sample") == "CMZ"
    assert solution.part_1("day05/input") == "TDCHVHJTG"


def test_part_2():
    assert solution.part_2("day05/sample") == "MCD"
    assert solution.part_2("day05/input") == "NGCMPJLHV"
