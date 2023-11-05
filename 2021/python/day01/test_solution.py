from day01 import solution


def test_part_1() -> None:
    assert solution.part_1("day01/sample") == 7
    assert solution.part_1("day01/input") == 1602


def test_part_2() -> None:
    assert solution.part_2("day01/sample") == 5
    assert solution.part_2("day01/input") == 1633
