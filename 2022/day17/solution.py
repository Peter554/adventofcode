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
class Rock:
    atoms: set[Point2D]

    def move(self, delta: Point2D) -> Rock:
        return Rock(set(p + delta for p in self.atoms))


rock_cycle = Cycle(
    (
        Rock({Point2D(1, 1), Point2D(2, 1), Point2D(3, 1), Point2D(4, 1)}),
        Rock(
            {Point2D(2, 1), Point2D(1, 2), Point2D(2, 2), Point2D(3, 2), Point2D(2, 3)}
        ),
        Rock(
            {Point2D(1, 1), Point2D(2, 1), Point2D(3, 1), Point2D(3, 2), Point2D(3, 3)}
        ),
        Rock({Point2D(1, 1), Point2D(1, 2), Point2D(1, 3), Point2D(1, 4)}),
        Rock({Point2D(1, 1), Point2D(2, 1), Point2D(1, 2), Point2D(2, 2)}),
    )
)


@dataclasses.dataclass
class RockChamber:
    width: int
    air_cycle: Cycle[Point2D]
    rock_cycle: Cycle[Rock]
    rocks: set[Rock]

    def drop_rock(self):
        ...


def part_1(file_path: str) -> int:
    with open(file_path) as f:
        air_cycle = parse_air_cycle(f.readline().strip())

    rock_chamber = RockChamber(7, air_cycle, rock_cycle, set())
    for _ in range(2022):
        rock_chamber.drop_rock()
    return max(atom.y for rock in rock_chamber.rocks for atom in rock.atoms)


def part_2(file_path: str) -> int:
    return 1
