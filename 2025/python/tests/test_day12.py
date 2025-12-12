from pathlib import Path

from aoc2025 import day12

DATA_DIR = Path(__file__).parent.parent / "data/day12"


def test_part_1(benchmark):
    # assert day12.part_1(DATA_DIR / "example.txt") == 2
    assert benchmark(lambda: day12.part_1(DATA_DIR / "input.txt")) == 425
