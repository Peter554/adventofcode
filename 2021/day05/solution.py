from __future__ import annotations

import copy
import collections


class Point:
    def __init__(self, *, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def __add__(self, other: Point) -> Point:
        return Point(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(x=self.x - other.x, y=self.y - other.y)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return False
        return (self.x == other.x) and (self.y == other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))


class Path:
    """A vertical, horizontal or 45°-diagonal path of points."""

    def __init__(self, *, x1: int, y1: int, x2: int, y2: int):
        self._points: list[Point] = self._get_points(x1, y1, x2, y2)

    def __repr__(self) -> str:
        return "Path(" + "->".join([repr(p) for p in self._points]) + ")"

    @property
    def points(self) -> list[Point]:
        return copy.deepcopy(self._points)

    @property
    def is_diagonal(self) -> bool:
        delta = self._points[-1] - self._points[0]
        return delta.x != 0 and delta.y != 0

    @staticmethod
    def _get_points(x1: int, y1: int, x2: int, y2: int) -> list[Point]:
        points: list[Point] = [
            Point(
                x=x1,
                y=y1,
            )
        ]
        last_point = Point(
            x=x2,
            y=y2,
        )
        if last_point == points[0]:
            return points
        delta = last_point - points[0]
        assert (
            (abs(delta.x) == abs(delta.y)) or delta.x == 0 or delta.y == 0
        ), "Invalid path angle."  # sanity check
        if abs(delta.x) > 0:
            delta.x = int(delta.x / abs(delta.x))
        if abs(delta.y) > 0:
            delta.y = int(delta.y / abs(delta.y))
        while True:
            points.append(points[-1] + delta)
            if points[-1] == last_point:
                break
        return points


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
