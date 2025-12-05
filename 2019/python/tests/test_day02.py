from pathlib import Path

from aoc2019 import day02

DATA_DIR = Path(__file__).parent.parent / "data/day02"


def test_part1():
    assert day02.part1(DATA_DIR / "input.txt") == 4930687


def test_part2():
    assert day02.part2(DATA_DIR / "input.txt") == 5335
