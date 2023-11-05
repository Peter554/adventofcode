from day11 import solution


def test_part_1() -> None:
    assert solution.part_1("day11/sample") == 1656
    assert solution.part_1("day11/input") == 1785


def test_part_2() -> None:
    assert solution.part_2("day11/sample") == 195
    assert solution.part_2("day11/input") == 354
