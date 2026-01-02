from pathlib import Path

from aoc2024 import day06

DATA_DIR = Path(__file__).parent.parent / "data/day06"


def test_part_1():
    assert day06.part_1(DATA_DIR / "example.txt") == 41
    assert day06.part_1(DATA_DIR / "input.txt") == 5208


def test_part_2():
    assert day06.part_2(DATA_DIR / "example.txt") == 6
    # assert day06.part_2(DATA_DIR / "input.txt") == 1972
