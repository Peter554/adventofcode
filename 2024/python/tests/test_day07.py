from pathlib import Path

from aoc2024 import day07

DATA_DIR = Path(__file__).parent.parent / "data/day07"


def test_part_1():
    assert day07.part_1(DATA_DIR / "example.txt") == 3749
    assert day07.part_1(DATA_DIR / "input.txt") == 20281182715321


def test_part_2():
    assert day07.part_2(DATA_DIR / "example.txt") == 11387
    assert day07.part_2(DATA_DIR / "input.txt") == 159490400628354
