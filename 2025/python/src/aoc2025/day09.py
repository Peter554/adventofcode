from __future__ import annotations

import dataclasses
import functools
import itertools
from pathlib import Path


def part_1(input: Path) -> int:
    red_tiles = parse_input(input)
    return max(
        [Rectange(p1, p2).area for p1, p2 in itertools.combinations(red_tiles, 2)]
    )


def part_2(input: Path) -> int:
    red_tiles = parse_input(input)
    rectanges = [Rectange(p1, p2) for p1, p2 in itertools.combinations(red_tiles, 2)]
    polygon = RectilinearPolygon(red_tiles)
    for rectange in sorted(
        rectanges,
        key=lambda r: r.area,
        reverse=True,
    ):
        if (
            # Check vertices first to speed up rejection.
            all(polygon.contains_point(p) for p in rectange.vertices)
            and
            # If all vertices are contained then check the entire perimeter.
            all(polygon.contains_point(p) for p in rectange.perimeter_points)
        ):
            # If all the rectange perimeter points are contained within the polygon,
            # then the rectangle is contained within the polygon (since this is a
            # rectilinear polygon).
            return rectange.area
    return -1


def parse_input(input: Path) -> tuple[Point, ...]:
    return tuple(
        Point(int(line.split(",")[0]), int(line.split(",")[1]))
        for line in input.read_text().splitlines()
    )


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)


@dataclasses.dataclass(frozen=True)
class Rectange:
    p1: Point
    p2: Point

    @functools.cached_property
    def area(self) -> int:
        return (abs(self.p2.x - self.p1.x) + 1) * (abs(self.p2.y - self.p1.y) + 1)

    @functools.cached_property
    def vertices(self) -> tuple[Point, ...]:
        min_x, max_x = min(self.p1.x, self.p2.x), max(self.p1.x, self.p2.x)
        min_y, max_y = min(self.p1.y, self.p2.y), max(self.p1.y, self.p2.y)
        return (
            Point(min_x, min_y),
            Point(max_x, min_y),
            Point(max_x, max_y),
            Point(min_x, max_y),
        )

    @property
    def perimeter_points(self) -> frozenset[Point]:
        return frozenset(perimeter_points(self.vertices))


@dataclasses.dataclass(frozen=True)
class RectilinearPolygon:
    vertices: tuple[Point, ...]

    @functools.cached_property
    def perimeter_points(self) -> frozenset[Point]:
        return frozenset(perimeter_points(self.vertices))

    def contains_point(self, p: Point) -> bool:
        if p in self.perimeter_points:
            # `p` is in the perimeter.
            return True

        # `p` is not in the perimeter.
        # Cast a horizontal ray from `p` to infinity.
        # Look for an odd number of crossings of verticle edges.
        crossings = 0
        for p1, p2 in zip(self.vertices, [*self.vertices[1:], self.vertices[0]]):
            y_min, y_max = min(p1.y, p2.y), max(p1.y, p2.y)
            if (
                # Verticle edge
                p1.x == p2.x
                and
                # Edge is to the right of `p`.
                p.x < p1.x
                and
                # Edge is crossed by ray from `p`.
                (y_min <= p.y < y_max)
            ):
                crossings += 1
        return crossings % 2 == 1


def perimeter_points(vertices: tuple[Point, ...]) -> tuple[Point, ...]:
    points = []
    for p1, p2 in zip(vertices, [*vertices[1:], vertices[0]]):
        if p1.x == p2.x:
            delta = Point(0, 1) if p1.y < p2.y else Point(0, -1)
        else:
            delta = Point(1, 0) if p1.x < p2.x else Point(-1, 0)
        p = p1
        while p != p2:
            points.append(p)
            p += delta
    return tuple(points)
