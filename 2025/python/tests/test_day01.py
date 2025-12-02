from pathlib import Path

from aoc2025 import day01

DATA_DIR = Path(__file__).parent.parent / "data/day01"


def test_part_1(benchmark):
    assert benchmark(lambda: day01.part_1(DATA_DIR / "input.txt")) == 980


def test_part_2(benchmark):
    assert benchmark(lambda: day01.part_2(DATA_DIR / "input.txt")) == 5961
