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


def parse_air_current(s: str) -> Cycle[Point2D]:
    air_directions: list[Point2D] = []
    for char in s:
        air_directions.append(
            {
                "<": Point2D(-1, 0),
                ">": Point2D(1, 0),
            }[char]
        )
    return Cycle(tuple(air_directions))


def part_1(file_path: str) -> int:
    with open(file_path) as f:
        air_current = parse_air_current(f.readline().strip())

    return 1


def part_2(file_path: str) -> int:
    return 1
