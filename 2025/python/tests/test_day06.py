from pathlib import Path

from aoc2025 import day06

DATA_DIR = Path(__file__).parent.parent / "data/day06"


def test_transpose_text():
    assert (
        day06.transpose_text("""\
ab
cde
 f""")
        == """\
ac
bdf
 e"""
    )


def test_part_1(benchmark):
    assert day06.part_1(DATA_DIR / "example.txt") == 4277556
    assert benchmark(lambda: day06.part_1(DATA_DIR / "input.txt")) == 3525371263915


def test_part_2(benchmark):
    assert day06.part_2(DATA_DIR / "example.txt") == 3263827
    assert benchmark(lambda: day06.part_2(DATA_DIR / "input.txt")) == 6846480843636
