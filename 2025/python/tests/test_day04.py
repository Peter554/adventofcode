from pathlib import Path

from aoc2025 import day04

DATA_DIR = Path(__file__).parent.parent / "data/day04"


def test_part_1(benchmark):
    assert day04.part_1(DATA_DIR / "example.txt") == 13
    assert benchmark(lambda: day04.part_1(DATA_DIR / "input.txt")) == 1602


def test_part_2(benchmark):
    assert day04.part_2(DATA_DIR / "example.txt") == 43
    assert benchmark(lambda: day04.part_2(DATA_DIR / "input.txt")) == 9518
