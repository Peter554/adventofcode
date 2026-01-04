from pathlib import Path

from aoc2024 import day13

DATA_DIR = Path(__file__).parent.parent / "data/day13"


def test_part_1():
    assert day13.part_1(DATA_DIR / "example.txt") == 480
    assert day13.part_1(DATA_DIR / "input.txt") == 29517


def test_part_2():
    assert day13.part_2(DATA_DIR / "input.txt") == 103570327981381
