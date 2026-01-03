from __future__ import annotations

import collections
import dataclasses
import itertools
from pathlib import Path


def part_1(input: Path) -> int:
    antennas, bounds = parse_input(input)

    antinodes = set()
    for antenna_type in antennas:
        for antenna_a, antenna_b in itertools.combinations(antennas[antenna_type], 2):
            delta = antenna_b - antenna_a
            if is_in_bounds(antenna_b + delta, bounds):
                antinodes.add(antenna_b + delta)
            if is_in_bounds(antenna_a - delta, bounds):
                antinodes.add(antenna_a - delta)

    return len(antinodes)


def part_2(input: Path) -> int:
    antennas, bounds = parse_input(input)

    antinodes = set()
    for antenna_type in antennas:
        for antenna_a, antenna_b in itertools.combinations(antennas[antenna_type], 2):
            delta = antenna_b - antenna_a
            p = antenna_b
            while is_in_bounds(p, bounds):
                antinodes.add(p)
                p += delta
            p = antenna_a
            while is_in_bounds(p, bounds):
                antinodes.add(p)
                p -= delta

    return len(antinodes)


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)


def parse_input(input: Path) -> tuple[dict[str, list[Point]], Point]:
    antennas = collections.defaultdict(list)
    bounds = Point(-1, -1)
    for y, line in enumerate(input.read_text().splitlines()):
        for x, char in enumerate(line):
            bounds = Point(x, y)
            if char == ".":
                continue
            else:
                antennas[char].append(Point(x, y))
    return antennas, bounds


def is_in_bounds(p: Point, bounds: Point) -> bool:
    return p.x >= 0 and p.x <= bounds.x and p.y >= 0 and p.y <= bounds.y
