from __future__ import annotations

import collections
import dataclasses
import typing

from common.point2d import Point2D


@dataclasses.dataclass(frozen=True)
class Blizzard:
    width: int
    height: int
    right: frozenset[Point2D]
    down: frozenset[Point2D]
    left: frozenset[Point2D]
    up: frozenset[Point2D]

    @classmethod
    def parse(cls, s: str) -> Blizzard:
        right: set[Point2D] = set()
        down: set[Point2D] = set()
        left: set[Point2D] = set()
        up: set[Point2D] = set()
        null: set[Point2D] = set()
        for y, line in enumerate(s.splitlines()[1:-1]):
            for x, char in enumerate(line[1:-1]):
                {">": right, "v": down, "<": left, "^": up,}.get(
                    char, null
                ).add(Point2D(x, y))
        return cls(
            x + 1,
            y + 1,
            frozenset(right),
            frozenset(down),
            frozenset(left),
            frozenset(up),
        )

    def evolve(self) -> Blizzard:
        right = {Point2D((p.x + 1) % self.width, p.y) for p in self.right}
        down = {Point2D(p.x, (p.y + 1) % self.height) for p in self.down}
        left = {Point2D((p.x - 1) % self.width, p.y) for p in self.left}
        up = {Point2D(p.x, (p.y - 1) % self.height) for p in self.up}
        return Blizzard(
            self.width,
            self.height,
            frozenset(right),
            frozenset(down),
            frozenset(left),
            frozenset(up),
        )

    def contains(self, p: Point2D) -> bool:
        return p in self.right or p in self.down or p in self.left or p in self.up

    def simulate(self) -> typing.Callable[[int], Blizzard]:
        blizzard = self
        lcm = self.width * self.height
        lookup: dict[int, Blizzard] = {}
        for t in range(lcm):
            lookup[t] = blizzard
            blizzard = blizzard.evolve()

        def f(t: int) -> Blizzard:
            return lookup[t % lcm]

        return f


def part_1(file_path: str) -> int:
    with open(file_path) as f:
        blizzard_by_timestep = Blizzard.parse(f.read()).simulate()
    width, height = blizzard_by_timestep(0).width, blizzard_by_timestep(0).height
    origin = Point2D(0, -1)
    destination = Point2D(width - 1, height)

    q = collections.deque([(0, origin)])
    while True:
        next_timestep_states = set()
        while q:
            t, p = q.popleft()
            if p == destination:
                return t
            for delta in [
                Point2D(0, 0),
                Point2D(1, 0),
                Point2D(0, 1),
                Point2D(-1, 0),
                Point2D(0, -1),
            ]:
                next_p = p + delta
                if (
                    next_p.x < 0
                    or next_p.x > width - 1
                    or next_p.y < 0
                    or next_p.y > height - 1
                ) and next_p not in {origin, destination}:
                    continue
                next_blizzard = blizzard_by_timestep(t + 1)
                if next_blizzard.contains(next_p):
                    continue
                next_timestep_states.add((t + 1, next_p))
        q.extend(next_timestep_states)


def part_2(file_path: str) -> int:
    with open(file_path) as f:
        blizzard_by_timestep = Blizzard.parse(f.read()).simulate()
    width, height = blizzard_by_timestep(0).width, blizzard_by_timestep(0).height
    origin = Point2D(0, -1)
    destination = Point2D(width - 1, height)

    def get_time(origin: Point2D, destination: Point2D, start_time: int) -> int:
        q = collections.deque([(start_time, origin)])
        while True:
            next_timestep_states = set()
            while q:
                t, p = q.popleft()
                if p == destination:
                    return t
                for delta in [
                    Point2D(0, 0),
                    Point2D(1, 0),
                    Point2D(0, 1),
                    Point2D(-1, 0),
                    Point2D(0, -1),
                ]:
                    next_p = p + delta
                    if (
                        next_p.x < 0
                        or next_p.x > width - 1
                        or next_p.y < 0
                        or next_p.y > height - 1
                    ) and next_p not in {origin, destination}:
                        continue
                    next_blizzard = blizzard_by_timestep(t + 1)
                    if next_blizzard.contains(next_p):
                        continue
                    next_timestep_states.add((t + 1, next_p))
            q.extend(next_timestep_states)

    t1 = get_time(origin, destination, 0)
    t2 = get_time(destination, origin, t1)
    return get_time(origin, destination, t2)
