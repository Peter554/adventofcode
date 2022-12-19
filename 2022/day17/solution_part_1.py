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
    return Cycle(
        tuple(
            {
                "<": Point2D(-1, 0),
                ">": Point2D(1, 0),
            }[char]
            for char in s
        )
    )


@dataclasses.dataclass(frozen=True)
class Rock:
    atoms: frozenset[Point2D]

    def move(self, delta: Point2D) -> Rock:
        return Rock(frozenset(atom + delta for atom in self.atoms))


rock_cycle = Cycle(
    (
        Rock(
            frozenset(
                {
                    Point2D(1, 1),
                    Point2D(2, 1),
                    Point2D(3, 1),
                    Point2D(4, 1),
                }
            )
        ),
        Rock(
            frozenset(
                {
                    Point2D(2, 1),
                    Point2D(1, 2),
                    Point2D(2, 2),
                    Point2D(3, 2),
                    Point2D(2, 3),
                }
            )
        ),
        Rock(
            frozenset(
                {
                    Point2D(1, 1),
                    Point2D(2, 1),
                    Point2D(3, 1),
                    Point2D(3, 2),
                    Point2D(3, 3),
                }
            )
        ),
        Rock(
            frozenset(
                {
                    Point2D(1, 1),
                    Point2D(1, 2),
                    Point2D(1, 3),
                    Point2D(1, 4),
                }
            )
        ),
        Rock(
            frozenset(
                {
                    Point2D(1, 1),
                    Point2D(2, 1),
                    Point2D(1, 2),
                    Point2D(2, 2),
                }
            )
        ),
    )
)


@dataclasses.dataclass
class RockChamber:
    width: int
    air_cycle: Cycle[Point2D]
    rock_cycle: Cycle[Rock]
    rubble: set[Point2D]

    @property
    def height(self) -> int:
        if not self.rubble:
            return 0
        return max(atom.y for atom in self.rubble)

    def drop_rock(self):
        rock = next(self.rock_cycle).move(Point2D(2, self.height + 3))
        while True:
            air_movement = next(self.air_cycle)
            _, rock = self._try_move(rock, air_movement)
            moved, rock = self._try_move(rock, Point2D(0, -1))
            if not moved:
                self.rubble = self.rubble.union(rock.atoms)
                break

    def _try_move(self, rock: Rock, delta: Point2D) -> tuple[bool, Rock]:
        moved_rock = rock.move(delta)
        if min(atom.x for atom in moved_rock.atoms) < 1:
            return False, rock
        elif max(atom.x for atom in moved_rock.atoms) > self.width:
            return False, rock
        elif min(atom.y for atom in moved_rock.atoms) < 1:
            return False, rock
        elif moved_rock.atoms.intersection(self.rubble):
            return False, rock
        return True, moved_rock

    def __str__(self):
        s = ""
        for y in range(self.height, 0, -1):
            s += "|"
            for x in range(1, self.width + 1):
                s += "#" if Point2D(x, y) in self.rubble else "."
            s += "|\n"
        s += "+" + "-" * self.width + "+\n"
        return s


def solve(file_path: str) -> int:
    with open(file_path) as f:
        air_cycle = parse_air_cycle(f.readline().strip())
    rock_chamber = RockChamber(7, air_cycle, rock_cycle, set())
    for _ in range(2022):
        rock_chamber.drop_rock()
    return rock_chamber.height
