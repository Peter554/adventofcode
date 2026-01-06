from pathlib import Path

from aoc2024 import day17

DATA_DIR = Path(__file__).parent.parent / "data/day17"


def test_part_1():
    assert day17.part_1(DATA_DIR / "example.txt") == "4,6,3,5,6,3,5,2,1,0"
    assert day17.part_1(DATA_DIR / "input.txt") == "7,0,7,3,4,1,3,0,1"


def test_part_2():
    assert day17.part_2() == 156985331222018
