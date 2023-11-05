import random

from day16 import solution_part_2


def test_solve():
    random.seed(42)
    assert solution_part_2.solve("day16/sample") == 1707
    # assert solution_part_2.solve("day16/input") == 2455
