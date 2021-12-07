from day07 import solution


def test_part_1() -> None:
    assert solution.part_1("day07/sample") == 37
    assert solution.part_1("day07/input") == 344735


def test_part_2() -> None:
    assert solution.part_2("day07/sample") == 168
    assert solution.part_2("day07/input") == 96798233
