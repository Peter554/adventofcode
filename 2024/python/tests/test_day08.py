from pathlib import Path

from aoc2024 import day08

DATA_DIR = Path(__file__).parent.parent / "data/day08"


def test_part_1():
    assert day08.part_1(DATA_DIR / "example.txt") == 14
    assert day08.part_1(DATA_DIR / "input.txt") == 381


def test_part_2():
    assert day08.part_2(DATA_DIR / "example.txt") == 34
    assert day08.part_2(DATA_DIR / "input.txt") == 1184
