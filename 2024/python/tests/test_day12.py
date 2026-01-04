from pathlib import Path

from aoc2024 import day12

DATA_DIR = Path(__file__).parent.parent / "data/day12"


def test_part_1():
    assert day12.part_1(DATA_DIR / "example.txt") == 1930
    assert day12.part_1(DATA_DIR / "input.txt") == 1371306


def test_part_2():
    assert day12.part_2(DATA_DIR / "example.txt") == 1206
    assert day12.part_2(DATA_DIR / "input.txt") == 805880
