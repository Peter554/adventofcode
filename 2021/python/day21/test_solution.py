from day21 import solution


def test_part_1() -> None:
    assert solution.part_1(3, 7) == 739785
    assert solution.part_1(1, 0) == 797160


def test_part_2() -> None:
    assert solution.part_2(3, 7) == 444356092776315
    assert solution.part_2(1, 0) == 27464148626406
