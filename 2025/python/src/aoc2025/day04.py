from pathlib import Path


def part_1(input: Path) -> int:
    grid = [[c == "@" for c in row] for row in input.read_text().splitlines()]
    return len(find_accessible_rolls(grid))


def part_2(input: Path) -> int:
    grid = [[c == "@" for c in row] for row in input.read_text().splitlines()]
    count_rolls_removed = 0
    while accessible_rolls := find_accessible_rolls(grid):
        for y, x in accessible_rolls:
            grid[y][x] = False
        count_rolls_removed += len(accessible_rolls)
    return count_rolls_removed


def find_accessible_rolls(grid: list[list[bool]]) -> set[tuple[int, int]]:
    accessible_rolls: set[tuple[int, int]] = set()
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] and is_accessible(grid, y, x):
                accessible_rolls.add((y, x))
    return accessible_rolls


def is_accessible(grid: list[list[bool]], y: int, x: int) -> bool:
    count = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy == 0 and dx == 0:
                continue
            if y + dy < 0 or y + dy >= len(grid):
                continue
            if x + dx < 0 or x + dx >= len(grid[0]):
                continue
            if grid[y + dy][x + dx]:
                count += 1
    return count < 4
