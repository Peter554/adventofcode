from pathlib import Path

from aoc2019 import day07

DATA_DIR = Path(__file__).parent.parent / "data/day07"


def test_part1():
    assert day07.part1(DATA_DIR / "input.txt") == 117312


def test_part2():
    assert day07.part2(DATA_DIR / "input.txt") == 1336480
