from day22 import solution


def test_part_1() -> None:
    assert solution.part_1("day22/sample") == 590784
    assert solution.part_1("day22/input") == 537042


def test_part_2() -> None:
    assert solution.part_2("day22/sample2") == 2758514936282235
    assert solution.part_2("day22/input") == 1304385553084863
