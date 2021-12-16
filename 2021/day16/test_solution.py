from day16 import solution


def test_part_1() -> None:
    assert solution.part_1("day16/sample1") == 16
    assert solution.part_1("day16/sample2") == 12
    assert solution.part_1("day16/sample3") == 23
    assert solution.part_1("day16/sample4") == 31
    assert solution.part_1("day16/input") == 866


def test_part_2() -> None:
    assert solution.part_2("day16/input") == 1392637195518
