from day04 import solution


def test_part_1() -> None:
    assert solution.part_1("day04/sample") == 4512
    assert solution.part_1("day04/input") == 33462


def test_part_2() -> None:
    assert solution.part_2("day04/sample") == 1924
    assert solution.part_2("day04/input") == 30070
