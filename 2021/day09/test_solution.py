from day09 import solution


def test_part_1() -> None:
    assert solution.part_1("day09/sample") == 15
    assert solution.part_1("day09/input") == 504


def test_part_2() -> None:
    assert solution.part_2("day09/sample") == 1134
    assert solution.part_2("day09/input") == 1558722
