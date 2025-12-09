from __future__ import annotations

import dataclasses
import functools
import itertools
from collections.abc import Iterable
from pathlib import Path

import numba
import numpy as np


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
        if polygon.contains_rectange(rectange):
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

    @functools.cached_property
    def perimeter_points(self) -> tuple[Point, ...]:
        return tuple(_perimeter_points(self.vertices))


@dataclasses.dataclass(frozen=True)
class RectilinearPolygon:
    vertices: tuple[Point, ...]

    def contains_rectange(self, rectange: Rectange) -> bool:
        if not self._contains_points(rectange.vertices):
            return False

        if not self._contains_points(rectange.perimeter_points[::100]):
            return False

        return self._contains_points(rectange.perimeter_points)

    def _contains_points(self, points: Iterable[Point]) -> bool:
        points_x = np.array([p.x for p in points], dtype=np.int_)
        points_y = np.array([p.y for p in points], dtype=np.int_)
        vertices_x, vertices_y = self._vertices_as_arrays
        return bool(
            np.all(
                _points_are_contained_by_polygon(
                    points_x, points_y, vertices_x, vertices_y
                )
            )
        )

    @functools.cached_property
    def _vertices_as_arrays(self):
        vertices_x = np.array([v.x for v in self.vertices], dtype=np.int_)
        vertices_y = np.array([v.y for v in self.vertices], dtype=np.int_)
        return vertices_x, vertices_y


def _perimeter_points(vertices: tuple[Point, ...]) -> tuple[Point, ...]:
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


@numba.njit
def _points_are_contained_by_polygon(
    points_x,
    points_y,
    polygon_vertices_x,
    polygon_vertices_y,
):
    n_points = len(points_x)
    results = np.empty(n_points, dtype=numba.boolean)
    for i in range(n_points):
        results[i] = _point_is_contained_by_polygon(
            points_x[i], points_y[i], polygon_vertices_x, polygon_vertices_y
        )
    return results


@numba.njit
def _point_is_contained_by_polygon(
    px,
    py,
    polygon_vertices_x,
    polygon_vertices_y,
):
    # Iterate over edges.
    # Look for:
    # * Point is part of the edge.
    # * Crossings of vertical edges for a horizontal ray from (px, py) to infinity.
    crossings = 0
    n = len(polygon_vertices_x)
    for i in range(n):
        p1x, p1y = polygon_vertices_x[i], polygon_vertices_y[i]
        p2x, p2y = polygon_vertices_x[(i + 1) % n], polygon_vertices_y[(i + 1) % n]

        x_min = min(p1x, p2x)
        x_max = max(p1x, p2x)
        y_min = min(p1y, p2y)
        y_max = max(p1y, p2y)

        # Check if (px, py) is part of the edge.
        if px == p1x == p2x and y_min <= py <= y_max:
            return True
        if py == p1y == p2y and x_min <= px <= x_max:
            return True

        # Check if this is a vertical edge that crosses our ray.
        if p1x == p2x and px < p1x and y_min <= py < y_max:
            crossings += 1
    return crossings % 2 == 1
