from pathlib import Path

from aoc2024 import day14

DATA_DIR = Path(__file__).parent.parent / "data/day14"


def test_part_1():
    assert day14.part_1(DATA_DIR / "example.txt", 11, 7) == 12
    assert day14.part_1(DATA_DIR / "input.txt", 101, 103) == 231782040


def test_part_2():
    assert day14.part_2(DATA_DIR / "input.txt", 101, 103) == 6475
