from pathlib import Path

from aoc2019 import day05

DATA_DIR = Path(__file__).parent.parent / "data/day05"


def test_part1():
    assert day05.part1(DATA_DIR / "input.txt") == 9219874


def test_part2():
    assert day05.part2(DATA_DIR / "input.txt") == 5893654
