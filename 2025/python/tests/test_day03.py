from pathlib import Path

from aoc2025 import day03

DATA_DIR = Path(__file__).parent.parent / "data/day03"


def test_part_1(benchmark):
    assert day03.part_1(DATA_DIR / "example.txt") == 357
    assert benchmark(lambda: day03.part_1(DATA_DIR / "input.txt")) == 17207


def test_part_2(benchmark):
    assert day03.part_2(DATA_DIR / "example.txt") == 3121910778619
    assert benchmark(lambda: day03.part_2(DATA_DIR / "input.txt")) == 170997883706617
