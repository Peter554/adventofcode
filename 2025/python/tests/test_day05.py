from pathlib import Path

from aoc2025 import day05

DATA_DIR = Path(__file__).parent.parent / "data/day05"


def test_part_1(benchmark):
    assert day05.part_1(DATA_DIR / "example.txt") == 3
    assert benchmark(lambda: day05.part_1(DATA_DIR / "input.txt")) == 598


def test_part_2(benchmark):
    assert day05.part_2(DATA_DIR / "example.txt") == 14
    assert benchmark(lambda: day05.part_2(DATA_DIR / "input.txt")) == 360341832208407
