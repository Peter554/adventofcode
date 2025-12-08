from __future__ import annotations

import dataclasses
from pathlib import Path


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def distance(self, other: Point) -> int:
        return (
            (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
        )


def part_1(input: Path, pairs_to_connect: int) -> int:
    points = parse_points(input)

    distances = compute_distances(points)

    circuits = {p: frozenset([p]) for p in points}
    pairs_connected = 0
    while pairs_connected < pairs_to_connect:
        _, p1, p2 = distances.pop()
        pairs_connected += 1
        if p2 not in circuits[p1]:
            connected_circuit = circuits[p1] | circuits[p2]
            for p in connected_circuit:
                circuits[p] = connected_circuit

    circuit_sizes = sorted(
        [len(circuit) for circuit in set(circuits.values())], reverse=True
    )
    return circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]


def part_2(input: Path) -> int:
    points = parse_points(input)

    distances = compute_distances(points)

    circuits = {p: frozenset([p]) for p in points}
    while True:
        _, p1, p2 = distances.pop()
        if p2 not in circuits[p1]:
            connected_circuit = circuits[p1] | circuits[p2]
            if len(connected_circuit) == len(points):
                return p1.x * p2.x
            for p in connected_circuit:
                circuits[p] = connected_circuit


def parse_points(input: Path) -> list[Point]:
    points: list[Point] = []
    for line in input.read_text().splitlines():
        x, y, z = [int(n) for n in line.split(",")]
        points.append(Point(x, y, z))
    return points


def compute_distances(points: list[Point]) -> list[tuple[int, Point, Point]]:
    distances = []
    for i, p1 in enumerate(points):
        for p2 in points[i + 1 :]:
            distances.append((p1.distance(p2), p1, p2))
    return sorted(distances, key=lambda x: x[0], reverse=True)
