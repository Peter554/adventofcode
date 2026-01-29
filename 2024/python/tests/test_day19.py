from pathlib import Path

from aoc2024 import day19

DATA_DIR = Path(__file__).parent.parent / "data/day19"


def test_part_1():
    assert day19.part_1(DATA_DIR / "example.txt") == 6
    assert day19.part_1(DATA_DIR / "input.txt") == 350


def test_part_2():
    assert day19.part_2(DATA_DIR / "example.txt") == 16
    assert day19.part_2(DATA_DIR / "input.txt") == 769668867512623
