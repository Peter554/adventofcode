from __future__ import annotations

import dataclasses
import collections


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Point) -> Point:
        return Point(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(x=self.x - other.x, y=self.y - other.y)


class Path:
    """A vertical, horizontal or 45°-diagonal path of points."""

    def __init__(self, *, x1: int, y1: int, x2: int, y2: int):
        self.points: tuple[Point, ...] = self._get_points(x1, y1, x2, y2)

    @property
    def is_diagonal(self) -> bool:
        delta = self.points[-1] - self.points[0]
        return delta.x != 0 and delta.y != 0

    @staticmethod
    def _get_points(x1: int, y1: int, x2: int, y2: int) -> tuple[Point, ...]:
        points: list[Point] = [Point(x=x1, y=y1)]
        last_point = Point(x=x2, y=y2)
        if last_point == points[0]:
            return tuple(points)
        delta = last_point - points[0]
        assert (
            (abs(delta.x) == abs(delta.y)) or delta.x == 0 or delta.y == 0
        ), "Invalid path angle."  # sanity check
        delta = Point(
            x=int(delta.x / abs(delta.x)) if delta.x else 0,
            y=int(delta.y / abs(delta.y)) if delta.y else 0,
        )
        while True:
            points.append(points[-1] + delta)
            if points[-1] == last_point:
                break
        return tuple(points)


def part_1(file_path: str) -> int:
    with open(file_path, "r") as f:
        lines = f.read().splitlines()

    paths = [
        Path(
            x1=int(line.split("->")[0].split(",")[0]),
            y1=int(line.split("->")[0].split(",")[1]),
            x2=int(line.split("->")[1].split(",")[0]),
            y2=int(line.split("->")[1].split(",")[1]),
        )
        for line in lines
    ]

    vents: dict[Point, int] = collections.defaultdict(lambda: 0)
    for path in paths:
        if path.is_diagonal:
            continue
        for point in path.points:
            vents[point] += 1
    return sum([v > 1 for v in vents.values()])


def part_2(file_path: str) -> int:
    with open(file_path, "r") as f:
        lines = f.read().splitlines()

    paths = [
        Path(
            x1=int(line.split("->")[0].split(",")[0]),
            y1=int(line.split("->")[0].split(",")[1]),
            x2=int(line.split("->")[1].split(",")[0]),
            y2=int(line.split("->")[1].split(",")[1]),
        )
        for line in lines
    ]

    vents: dict[Point, int] = collections.defaultdict(lambda: 0)
    for path in paths:
        for point in path.points:
            vents[point] += 1
    return sum([v > 1 for v in vents.values()])
