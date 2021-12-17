from day17 import solution


def test_part_1() -> None:
    assert solution.part_1(20, 30, -10, -5) == 45
    assert solution.part_1(124, 174, -123, -86) == 7503


def test_part_2() -> None:
    assert solution.part_2(20, 30, -10, -5) == 112
    assert solution.part_2(124, 174, -123, -86) == 3229
