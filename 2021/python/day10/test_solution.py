from day10 import solution


def test_part_1() -> None:
    assert solution.part_1("day10/sample") == 26397
    assert solution.part_1("day10/input") == 358737


def test_part_2() -> None:
    assert solution.part_2("day10/sample") == 288957
    assert solution.part_2("day10/input") == 4329504793
