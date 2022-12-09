from __future__ import annotations

import dataclasses
from typing import Literal


@dataclasses.dataclass(frozen=True)
class Point2D:
    x: int
    y: int

    def __add__(self, other: Point2D) -> Point2D:
        return Point2D(self.x + other.x, self.y + other.y)

    def __mul__(self, f: int) -> Point2D:
        return Point2D(self.x * f, self.y * f)

    def touching(self, other: Point2D) -> bool:
        return max(abs(self.x - other.x), abs(self.y - other.y)) <= 1


Direction = Literal["U", "D", "L", "R"]


def parse_direction(s: str) -> Direction:
    mapping: dict[str, Direction] = {"U": "U", "D": "D", "L": "L", "R": "R"}
    return mapping[s]


class Rope:
    _DIRECTION_DELTA_MAPPING: dict[Direction, Point2D] = {
        "U": Point2D(0, 1),
        "D": Point2D(0, -1),
        "L": Point2D(-1, 0),
        "R": Point2D(1, 0),
    }

    def __init__(self, length: int):
        self._state = [Point2D(0, 0) for _ in range(length)]

    @property
    def state(self) -> tuple[Point2D, ...]:
        return tuple(self._state)

    def evolve(self, direction: Direction) -> None:
        next_state = [self._state[0] + self._DIRECTION_DELTA_MAPPING[direction]]
        for idx in range(1, len(self._state)):
            delta = self._get_delta(self._state[idx], next_state[idx - 1])
            next_state.append(self._state[idx] + delta)
        self._state = next_state

    @staticmethod
    def _get_delta(tail: Point2D, head: Point2D) -> Point2D:
        if tail.touching(head):
            return Point2D(0, 0)
        # same row/column: move horizontal
        # else: move diagonal
        return Point2D(
            (head.x - tail.x) // (abs(head.x - tail.x) or 1),
            (head.y - tail.y) // (abs(head.y - tail.y) or 1),
        )


def solve_puzzle(file_path: str, rope_length: int) -> int:
    with open(file_path) as f:
        instructions = [line.strip() for line in f.readlines()]
    rope = Rope(rope_length)
    rope_tail_history = {rope.state[-1]}
    for instruction in instructions:
        direction, count = instruction.split(" ")
        for _ in range(int(count)):
            rope.evolve(parse_direction(direction))
            rope_tail_history.add(rope.state[-1])
    return len(rope_tail_history)


def part_1(file_path: str) -> int:
    return solve_puzzle(file_path, 2)


def part_2(file_path: str) -> int:
    return solve_puzzle(file_path, 10)
