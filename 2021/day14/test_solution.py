from day14 import solution


def test_part_1() -> None:
    assert solution.part_1("day14/sample") == 1588
    assert solution.part_1("day14/input") == 2657


def test_part_2() -> None:
    assert solution.part_2("day14/sample") == 2188189693529
    assert solution.part_2("day14/input") == 2911561572630
