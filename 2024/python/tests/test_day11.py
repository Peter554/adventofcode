from pathlib import Path

from aoc2024 import day11

DATA_DIR = Path(__file__).parent.parent / "data/day11"


def test_part_1():
    assert day11.part_1(DATA_DIR / "example.txt") == 55312
    assert day11.part_1(DATA_DIR / "input.txt") == 199982


def test_part_2():
    assert day11.part_2(DATA_DIR / "input.txt") == 237149922829154
