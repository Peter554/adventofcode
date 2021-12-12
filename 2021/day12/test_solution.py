from day12 import solution


def test_part_1() -> None:
    assert solution.part_1("day12/sample") == 10
    assert solution.part_1("day12/input") == 4413


def test_part_2() -> None:
    assert solution.part_2("day12/sample") == 36
    assert solution.part_2("day12/input") == 118803
