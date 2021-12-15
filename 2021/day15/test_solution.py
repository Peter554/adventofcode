from day15 import solution


def test_part_1() -> None:
    assert solution.part_1("day15/sample") == 40
    assert solution.part_1("day15/input") == 685


def test_part_2() -> None:
    assert solution.part_2("day15/sample") == 315
    assert solution.part_2("day15/input") == 2995
