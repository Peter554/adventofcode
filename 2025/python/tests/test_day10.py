from pathlib import Path

from aoc2025 import day10

DATA_DIR = Path(__file__).parent.parent / "data/day10"


def test_part_1(benchmark):
    assert day10.part_1(DATA_DIR / "example.txt") == 7
    assert benchmark(lambda: day10.part_1(DATA_DIR / "input.txt")) == 455


def test_part_2(benchmark):
    assert day10.part_2(DATA_DIR / "example.txt") == 33
    assert benchmark(lambda: day10.part_2(DATA_DIR / "input.txt")) == 16978
