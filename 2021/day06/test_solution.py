from day06 import solution


def test_part_1() -> None:
    assert solution.part_1("day06/sample") == 5934
    assert solution.part_1("day06/input") == 366057


def test_part_2() -> None:
    assert solution.part_2("day06/sample") == 26984457539
    assert solution.part_2("day06/input") == 1653559299811
