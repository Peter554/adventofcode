from pathlib import Path

from aoc2024 import day18

DATA_DIR = Path(__file__).parent.parent / "data/day18"


def test_part_1():
    assert day18.part_1(DATA_DIR / "example.txt", 6, 12) == 22
    assert day18.part_1(DATA_DIR / "input.txt", 70, 1024) == 282


def test_part_2():
    assert day18.part_2(DATA_DIR / "example.txt", 6) == (6, 1)
    assert day18.part_2(DATA_DIR / "input.txt", 70) == (64, 29)
