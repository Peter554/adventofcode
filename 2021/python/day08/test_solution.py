from day08 import solution


def test_part_1() -> None:
    assert solution.part_1("day08/sample") == 0 + 26
    assert solution.part_1("day08/input") == 543


def test_part_2() -> None:
    assert solution.part_2("day08/sample") == 5353 + 61229
    assert solution.part_2("day08/input") == 994266
