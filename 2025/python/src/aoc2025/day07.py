import functools
from pathlib import Path

type Point = tuple[int, int]


def part_1(input: Path) -> int:
    grid = [[c for c in row] for row in input.read_text().splitlines()]
    source: Point = (0, grid[0].index("S"))

    beam_heads: set[Point] = {source}
    splitters_hit: set[Point] = set()
    while beam_heads:
        next_beam_heads: set[Point] = set()
        for head in beam_heads:
            if head[0] == len(grid) - 1:
                continue
            elif grid[head[0] + 1][head[1]] == ".":
                next_beam_heads.add((head[0] + 1, head[1]))
            elif grid[head[0] + 1][head[1]] == "^":
                splitters_hit.add((head[0] + 1, head[1]))
                next_beam_heads.add((head[0] + 1, head[1] + 1))
                next_beam_heads.add((head[0] + 1, head[1] - 1))
            else:
                assert False, "unexpected grid character"
        beam_heads = next_beam_heads

    return len(splitters_hit)


def part_2(input: Path) -> int:
    grid = [[c for c in row] for row in input.read_text().splitlines()]
    source: Point = (0, grid[0].index("S"))

    @functools.cache
    def follow_beam(head: Point) -> int:
        if head[0] == len(grid) - 1:
            return 1
        elif grid[head[0] + 1][head[1]] == ".":
            return follow_beam((head[0] + 1, head[1]))
        elif grid[head[0] + 1][head[1]] == "^":
            return follow_beam((head[0] + 1, head[1] + 1)) + follow_beam(
                (head[0] + 1, head[1] - 1)
            )
        else:
            assert False, "unexpect grid character"

    return follow_beam(source)
