from pathlib import Path

from aoc2024 import day16

DATA_DIR = Path(__file__).parent.parent / "data/day16"


def test_part_1():
    assert day16.part_1(DATA_DIR / "example_1.txt") == 7036
    assert day16.part_1(DATA_DIR / "example_2.txt") == 11048
    assert day16.part_1(DATA_DIR / "input.txt") == 127520


def test_part_2():
    assert day16.part_2(DATA_DIR / "example_1.txt") == 45
    assert day16.part_2(DATA_DIR / "example_2.txt") == 64
    assert day16.part_2(DATA_DIR / "input.txt") == 565
