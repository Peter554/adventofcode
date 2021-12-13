from day13 import solution


def test_part_1() -> None:
    assert solution.part_1("day13/sample") == 17
    assert solution.part_1("day13/input") == 745


def test_part_2() -> None:
    assert (
        solution.part_2("day13/sample")
        == """
#####
#...#
#...#
#...#
#####
""".strip()
    )

    # ABKJFBGC
    assert (
        solution.part_2("day13/input")
        == """
.##..###..#..#...##.####.###...##...##.
#..#.#..#.#.#.....#.#....#..#.#..#.#..#
#..#.###..##......#.###..###..#....#...
####.#..#.#.#.....#.#....#..#.#.##.#...
#..#.#..#.#.#..#..#.#....#..#.#..#.#..#
#..#.###..#..#..##..#....###...###..##.
""".strip()
    )
