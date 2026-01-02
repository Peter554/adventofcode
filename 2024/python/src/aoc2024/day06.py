from __future__ import annotations

import enum
import itertools
from pathlib import Path


def part_1(input: Path) -> int:
    start, obstacles, bounds = parse_input(input)

    position = start
    direction = Direction.UP
    visited = {start}
    while True:
        candidate_next_position = move_forward(position, direction)
        while candidate_next_position in obstacles:
            direction = direction.turn_right()
            candidate_next_position = move_forward(position, direction)
        position = candidate_next_position

        if is_out_of_bounds(position, bounds):
            break

        visited.add(position)

    return len(visited)


def part_2(input: Path) -> int:
    start, obstacles, bounds = parse_input(input)

    def check_cycle(obstacles: set[Point]) -> bool:
        position = start
        direction = Direction.UP
        visited = {(position, direction)}
        while True:
            candidate_next_position = move_forward(position, direction)
            while candidate_next_position in obstacles:
                direction = direction.turn_right()
                candidate_next_position = move_forward(position, direction)
            position = candidate_next_position

            if is_out_of_bounds(position, bounds):
                return False

            if (position, direction) in visited:
                return True
            else:
                visited.add((position, direction))

    count_cycles = 0
    for x, y in itertools.product(range(bounds[0] + 1), range(bounds[1] + 1)):
        if (x, y) == start:
            continue
        if check_cycle({*obstacles, (x, y)}):
            count_cycles += 1

    return count_cycles


Point = tuple[int, int]


class Direction(enum.IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def turn_right(self) -> Direction:
        return Direction((self + 1) % 4)

    def to_delta(self) -> Point:
        match self:
            case Direction.UP:
                # UP is towards y=0
                return 0, -1
            case Direction.RIGHT:
                return 1, 0
            case Direction.DOWN:
                return 0, 1
            case Direction.LEFT:
                return -1, 0


def parse_input(input: Path) -> tuple[Point, set[Point], Point]:
    start: Point | None = None
    obstacles: set[Point] = set()
    x_max: int = 0
    y_max: int = 0
    for y, line in enumerate(input.read_text().splitlines()):
        y_max = y
        for x, c in enumerate(line):
            x_max = x
            if c == "#":
                obstacles.add((x, y))
            elif c == "^":
                start = (x, y)
    assert start is not None
    return start, obstacles, (x_max, y_max)


def move_forward(p: Point, dir: Direction) -> Point:
    return (
        p[0] + dir.to_delta()[0],
        p[1] + dir.to_delta()[1],
    )


def is_out_of_bounds(p: Point, bounds: Point) -> bool:
    x_max, y_max = bounds
    return p[0] < 0 or p[0] > x_max or p[1] < 0 or p[1] > y_max
