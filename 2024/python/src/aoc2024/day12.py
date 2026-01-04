from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


def part_1(input: Path) -> int:
    grid = {
        P(x, y): c
        for y, line in enumerate(input.read_text().splitlines())
        for x, c in enumerate(line)
    }
    regions = discover_regions(grid)
    return sum(r.area * r.perimeter for r in regions)


def part_2(input: Path) -> int:
    grid = {
        P(x, y): c
        for y, line in enumerate(input.read_text().splitlines())
        for x, c in enumerate(line)
    }
    regions = discover_regions(grid)
    return sum(r.area * r.sides for r in regions)


@dataclass(frozen=True)
class P:
    x: int
    y: int

    def __add__(self, other: P) -> P:
        return P(self.x + other.x, self.y + other.y)

    @property
    def neighbors(self) -> frozenset[P]:
        return frozenset(
            self + delta for delta in (P(0, 1), P(0, -1), P(1, 0), P(-1, 0))
        )


def discover_regions(grid: dict[P, str]) -> tuple[Region, ...]:
    regions = []
    to_connect = set(grid.keys())
    while to_connect:
        q = [to_connect.pop()]
        region = set()
        while q:
            p = q.pop(0)
            if p in region:
                continue
            region.add(p)
            for neighbor in p.neighbors:
                if neighbor in grid and grid[neighbor] == grid[p]:
                    q.append(neighbor)
        regions.append(Region(frozenset(region)))
        to_connect -= region
    return tuple(regions)


@dataclass(frozen=True)
class Region:
    points: frozenset[P]

    @property
    def area(self) -> int:
        return len(self.points)

    @property
    def perimeter(self) -> int:
        return sum(
            1
            for p in self.points
            for neighbor in p.neighbors
            if neighbor not in self.points
        )

    @property
    def sides(self) -> int:
        # Sides => count corners, it's easier.
        corners = 0
        for p in self.points:
            for d1, d2 in (
                (P(1, 0), P(0, 1)),
                (P(0, 1), P(-1, 0)),
                (P(-1, 0), P(0, -1)),
                (P(0, -1), P(1, 0)),
            ):
                if p + d1 not in self.points and p + d2 not in self.points:
                    # Convex corner
                    corners += 1
                elif (
                    p + d1 in self.points
                    and p + d2 in self.points
                    and p + d1 + d2 not in self.points
                ):
                    # Concave corner
                    corners += 1

        return corners
