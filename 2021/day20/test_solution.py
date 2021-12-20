from day20 import solution


def test_part_1() -> None:
    assert solution.solve("day20/sample", 2) == 35
    assert solution.solve("day20/input", 2) == 5682


def test_part_2() -> None:
    assert solution.solve("day20/sample", 50) == 3351
    assert solution.solve("day20/input", 50) == 17628
