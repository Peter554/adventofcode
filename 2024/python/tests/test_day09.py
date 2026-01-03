from pathlib import Path

from aoc2024 import day09

DATA_DIR = Path(__file__).parent.parent / "data/day09"


def test_part_1():
    assert day09.part_1(DATA_DIR / "example.txt") == 1928
    assert day09.part_1(DATA_DIR / "input.txt") == 6384282079460


def test_part_2():
    assert day09.part_2(DATA_DIR / "example.txt") == 2858
    assert day09.part_2(DATA_DIR / "input.txt") == 6408966547049
