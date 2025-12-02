from pathlib import Path

from aoc2025 import day02

DATA_DIR = Path(__file__).parent.parent / "data/day02"


def test_part_1(benchmark):
    assert day02.part_1(DATA_DIR / "example.txt") == 1227775554
    assert benchmark(lambda: day02.part_1(DATA_DIR / "input.txt")) == 56660955519


def test_part_2(benchmark):
    assert day02.part_2(DATA_DIR / "example.txt") == 4174379265
    assert benchmark(lambda: day02.part_2(DATA_DIR / "input.txt")) == 79183223243
