from __future__ import annotations

import collections
import dataclasses
import typing

from common.point2d import Point2D, Box2D

ProposalFunction = typing.Callable[[Point2D], tuple[Point2D, set[Point2D]]]


def propose_north(p: Point2D):
    return (
        p + Point2D(0, -1),
        {p + Point2D(-1, -1), p + Point2D(0, -1), p + Point2D(1, -1)},
    )


def propose_south(p: Point2D):
    return (
        p + Point2D(0, 1),
        {p + Point2D(-1, 1), p + Point2D(0, 1), p + Point2D(1, 1)},
    )


def propose_east(p: Point2D):
    return (
        p + Point2D(1, 0),
        {p + Point2D(1, -1), p + Point2D(1, 0), p + Point2D(1, 1)},
    )


def propose_west(p: Point2D):
    return (
        p + Point2D(-1, 0),
        {p + Point2D(-1, -1), p + Point2D(-1, 0), p + Point2D(-1, 1)},
    )


def rotate(lst: list) -> list:
    return [*lst[1:], lst[0]]


@dataclasses.dataclass
class Elves:
    positions: set[Point2D]

    def __post_init__(self):
        self.proposal_functions = [
            propose_north,
            propose_south,
            propose_west,
            propose_east,
        ]

    @classmethod
    def parse(cls, s: str) -> Elves:
        positions: set[Point2D] = set()
        for y, line in enumerate(s.splitlines()):
            for x, char in enumerate(line.strip()):
                if char == "#":
                    positions.add(Point2D(x, y))
        return cls(positions)

    def evolve(self):
        proposals: dict[Point2D, list[Point2D]] = collections.defaultdict(list)
        for elf in self.positions:
            proposal = self.propose_move(elf)
            if proposal is not None:
                proposals[proposal].append(elf)
        moves = {v[0]: k for k, v in proposals.items() if len(v) == 1}
        if not moves:
            return False
        for move_from, move_to in moves.items():
            self.positions.remove(move_from)
            self.positions.add(move_to)
        self.proposal_functions = rotate(self.proposal_functions)
        return True

    def should_move(self, elf: Point2D):
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                if Point2D(elf.x + dx, elf.y + dy) in self.positions:
                    return True
        return False

    def propose_move(self, elf: Point2D):
        if not self.should_move(elf):
            return None
        for proposal_function in self.proposal_functions:
            proposal, check_points = proposal_function(elf)
            if check_points.intersection(self.positions) == set():
                return proposal
        return None


def count_empty(points: set[Point2D]) -> int:
    x_min = min(p.x for p in points)
    x_max = max(p.x for p in points)
    y_min = min(p.y for p in points)
    y_max = max(p.y for p in points)
    box = Box2D(Point2D(x_min, y_min), Point2D(x_max, y_max))
    return len(box.points - points)


def part_1(file_path: str) -> int:
    with open(file_path) as f:
        elves = Elves.parse(f.read())
    for _ in range(10):
        elves.evolve()
    return count_empty(elves.positions)


def part_2(file_path: str) -> int:
    with open(file_path) as f:
        elves = Elves.parse(f.read())
    round = 0
    while True:
        round += 1
        changed = elves.evolve()
        if not changed:
            return round
