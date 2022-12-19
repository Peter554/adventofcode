from __future__ import annotations

import dataclasses
from typing import Generic, TypeVar

from common.point2d import Point2D


TCycle = TypeVar("TCycle")


class Cycle(Generic[TCycle]):
    def __init__(self, t: tuple[TCycle, ...]):
        self._t = t
        self._i = 0

    def __next__(self):
        o = self._t[self._i]
        self._i = (self._i + 1) % len(self._t)
        return o


def parse_air_cycle(s: str) -> Cycle[Point2D]:
    air_directions: list[Point2D] = []
    for char in s:
        air_directions.append(
            {
                "<": Point2D(-1, 0),
                ">": Point2D(1, 0),
            }[char]
        )
    return Cycle(tuple(air_directions))


@dataclasses.dataclass(frozen=True)
class Shape:
    points: set[Point2D]

    def move(self, delta: Point2D) -> Shape:
        return Shape(set(p + delta for p in self.points))


rock_cycle = Cycle(
    (
        Shape({Point2D(1, 1), Point2D(2, 1), Point2D(3, 1), Point2D(4, 1)}),
        Shape(
            {Point2D(2, 1), Point2D(1, 2), Point2D(2, 2), Point2D(3, 2), Point2D(2, 3)}
        ),
        Shape(
            {Point2D(1, 1), Point2D(2, 1), Point2D(3, 1), Point2D(3, 2), Point2D(3, 3)}
        ),
        Shape({Point2D(1, 1), Point2D(1, 2), Point2D(1, 3), Point2D(1, 4)}),
        Shape({Point2D(1, 1), Point2D(2, 1), Point2D(1, 2), Point2D(2, 2)}),
    )
)


def part_1(file_path: str) -> int:
    with open(file_path) as f:
        air_cycle = parse_air_cycle(f.readline().strip())
    return 1


def part_2(file_path: str) -> int:
    return 1
