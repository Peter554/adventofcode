from pathlib import Path

from aoc2025 import day07

DATA_DIR = Path(__file__).parent.parent / "data/day07"


def test_part_1(benchmark):
    assert day07.part_1(DATA_DIR / "example.txt") == 21
    assert benchmark(lambda: day07.part_1(DATA_DIR / "input.txt")) == 1649


def test_part_2(benchmark):
    assert day07.part_2(DATA_DIR / "example.txt") == 40
    assert benchmark(lambda: day07.part_2(DATA_DIR / "input.txt")) == 16937871060075
