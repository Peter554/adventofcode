from __future__ import annotations

import dataclasses

from common.point2d import Point2D


def normalize(p: Point2D) -> Point2D:
    assert p.x == 0 or p.y == 0
    size = abs(p.x) + abs(p.y)
    return Point2D(p.x // size, p.y // size)


def parse_rock(raw_rocks: list[str]) -> set[Point2D]:
    rock: set[Point2D] = set()
    for raw_rock in raw_rocks:
        vertices = [
            Point2D(int(raw_vertex.split(",")[0]), int(raw_vertex.split(",")[1]))
            for raw_vertex in raw_rock.split(" -> ")
        ]
        for vertex_from, vertex_to in zip(vertices[:-1], vertices[1:]):
            delta = normalize(vertex_to - vertex_from)
            segment_rocks = [vertex_from]
            while vertex_to != segment_rocks[-1]:
                segment_rocks.append(segment_rocks[-1] + delta)
            rock.update(segment_rocks)
    return rock


@dataclasses.dataclass
class SandWorldV1:
    rock: set[Point2D]
    sand_falling: Point2D | None = None
    sand_resting: set[Point2D] = dataclasses.field(default_factory=set)

    @property
    def overflowing(self) -> bool:
        return self.sand_falling is not None and self.sand_falling.y > max(
            p.y for p in self.rock
        )

    def evolve(self) -> None:
        if self.sand_falling is None:
            self.sand_falling = Point2D(500, 0)
            return

        for delta in [Point2D(0, 1), Point2D(-1, 1), Point2D(1, 1)]:
            p = self.sand_falling + delta
            if p not in self.rock and p not in self.sand_resting:
                self.sand_falling = p
                return
        self.sand_resting.add(self.sand_falling)
        self.sand_falling = None


def part_1(file_path: str) -> int:
    with open(file_path) as f:
        raw_rocks = [line.strip() for line in f.readlines()]
    rock = parse_rock(raw_rocks)
    sandworld = SandWorldV1(rock)
    while not sandworld.overflowing:
        sandworld.evolve()
    return len(sandworld.sand_resting)


@dataclasses.dataclass
class SandWorldV2:
    rock: set[Point2D]
    sand_falling: Point2D | None = None
    sand_resting: set[Point2D] = dataclasses.field(default_factory=set)

    def __post_init__(self):
        self.floor = max(p.y for p in self.rock) + 2

    @property
    def overflowing(self) -> bool:
        return Point2D(500, 0) in self.sand_resting

    def evolve(self) -> None:
        if self.sand_falling is None:
            self.sand_falling = Point2D(500, 0)
            return

        for delta in [Point2D(0, 1), Point2D(-1, 1), Point2D(1, 1)]:
            p = self.sand_falling + delta
            if p not in self.rock and p not in self.sand_resting and p.y < self.floor:
                self.sand_falling = p
                return
        self.sand_resting.add(self.sand_falling)
        self.sand_falling = None


def part_2(file_path: str) -> int:
    with open(file_path) as f:
        raw_rocks = [line.strip() for line in f.readlines()]
    rock = parse_rock(raw_rocks)
    sandworld = SandWorldV2(rock)
    while not sandworld.overflowing:
        sandworld.evolve()
    return len(sandworld.sand_resting)
