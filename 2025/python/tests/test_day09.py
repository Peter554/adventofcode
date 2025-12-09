from pathlib import Path

from aoc2025 import day09

DATA_DIR = Path(__file__).parent.parent / "data/day09"


def test_part_1(benchmark):
    assert day09.part_1(DATA_DIR / "example.txt") == 50
    assert benchmark(lambda: day09.part_1(DATA_DIR / "input.txt")) == 4733727792


def test_part_2(benchmark):
    assert day09.part_2(DATA_DIR / "example.txt") == 24
    assert day09.part_2(DATA_DIR / "example2.txt") == 21
    assert benchmark(lambda: day09.part_2(DATA_DIR / "input.txt")) == 1566346198
