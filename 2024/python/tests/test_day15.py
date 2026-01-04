from pathlib import Path

from aoc2024 import day15

DATA_DIR = Path(__file__).parent.parent / "data/day15"


def test_part_1():
    assert day15.part_1(DATA_DIR / "example_small.txt") == 2028
    assert day15.part_1(DATA_DIR / "example_large.txt") == 10092
    assert day15.part_1(DATA_DIR / "input.txt") == 1442192


def test_part_2():
    assert day15.part_2(DATA_DIR / "example_large.txt") == 9021
    # assert day15.part_2(DATA_DIR / "input.txt") == 42
