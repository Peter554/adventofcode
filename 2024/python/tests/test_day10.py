from pathlib import Path

from aoc2024 import day10

DATA_DIR = Path(__file__).parent.parent / "data/day10"


def test_part_1():
    assert day10.part_1(DATA_DIR / "example.txt") == 36
    assert day10.part_1(DATA_DIR / "input.txt") == 557


def test_part_2():
    assert day10.part_2(DATA_DIR / "example.txt") == 81
    assert day10.part_2(DATA_DIR / "input.txt") == 1062
