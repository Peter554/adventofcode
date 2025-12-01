from pathlib import Path

from aoc2025 import day01

DATA_DIR = Path(__file__).parent.parent / "data"


def test_part_1():
    assert day01.part_1(DATA_DIR / "day01/input.txt") == 980


def test_part_2():
    assert day01.part_2(DATA_DIR / "day01/input.txt") == 5961
