from pathlib import Path

from aoc2025 import day08

DATA_DIR = Path(__file__).parent.parent / "data/day08"


def test_part_1(benchmark):
    assert day08.part_1(DATA_DIR / "example.txt", 10) == 40
    assert benchmark(lambda: day08.part_1(DATA_DIR / "input.txt", 1000)) == 79056


def test_part_2(benchmark):
    assert day08.part_2(DATA_DIR / "example.txt") == 25272
    assert benchmark(lambda: day08.part_2(DATA_DIR / "input.txt")) == 4639477
