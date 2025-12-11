from pathlib import Path

from aoc2025 import day11

DATA_DIR = Path(__file__).parent.parent / "data/day11"


def test_part_1(benchmark):
    assert day11.part_1(DATA_DIR / "example.txt") == 5
    assert benchmark(lambda: day11.part_1(DATA_DIR / "input.txt")) == 555


def test_part_2(benchmark):
    assert day11.part_2(DATA_DIR / "example2.txt") == 2
    assert benchmark(lambda: day11.part_2(DATA_DIR / "input.txt")) == 502447498690860
