import functools
from pathlib import Path


def part_1(input: Path) -> int:
    grid = [list(map(int, line)) for line in input.read_text().splitlines()]
    trailheads = [
        (row, col)
        for row in range(len(grid))
        for col in range(len(grid[0]))
        if grid[row][col] == 0
    ]

    @functools.cache
    def follow_trail(th: tuple[int, int]) -> set[tuple[int, int]]:
        if grid[th[0]][th[1]] == 9:
            return {th}
        else:
            ends = set()
            for neighbor in get_neighbors(th, grid):
                if grid[neighbor[0]][neighbor[1]] == grid[th[0]][th[1]] + 1:
                    ends.update(follow_trail(neighbor))
            return ends

    return sum(len(follow_trail(th)) for th in trailheads)


def part_2(input: Path) -> int:
    grid = [list(map(int, line)) for line in input.read_text().splitlines()]
    trailheads = [
        (row, col)
        for row in range(len(grid))
        for col in range(len(grid[0]))
        if grid[row][col] == 0
    ]

    @functools.cache
    def count_trails(th: tuple[int, int]) -> int:
        if grid[th[0]][th[1]] == 9:
            return 1
        else:
            return sum(
                count_trails(neighbor)
                for neighbor in get_neighbors(th, grid)
                if grid[neighbor[0]][neighbor[1]] == grid[th[0]][th[1]] + 1
            )

    return sum(count_trails(th) for th in trailheads)


def get_neighbors(th: tuple[int, int], grid: list[list[int]]) -> list[tuple[int, int]]:
    row, col = th
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))
    if row < len(grid) - 1:
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if col < len(grid[0]) - 1:
        neighbors.append((row, col + 1))
    return neighbors
