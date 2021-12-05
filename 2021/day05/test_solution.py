from day05 import solution


def test_part_1() -> None:
    assert solution.part_1("day05/sample") == 5
    assert solution.part_1("day05/input") == 6841


def test_part_2() -> None:
    assert solution.part_2("day05/sample") == 12
    assert solution.part_2("day05/input") == 19258
