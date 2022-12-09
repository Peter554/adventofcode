from __future__ import annotations

import dataclasses


@dataclasses.dataclass(frozen=True)
class Point2D:
    x: int
    y: int

    def __add__(self, other: Point2D) -> Point2D:
        return Point2D(self.x + other.x, self.y + other.y)

    def __mul__(self, f: int) -> Point2D:
        return Point2D(self.x * f, self.y * f)

    def touching(self, other: Point2D) -> bool:
        return max(abs(self.x - other.x), abs(self.y - other.y)) <= 1


DIRECTION_MAPPING = {
    "R": Point2D(1, 0),
    "L": Point2D(-1, 0),
    "U": Point2D(0, 1),
    "D": Point2D(0, -1),
}


def part_1(file_path: str) -> int:
    with open(file_path) as f:
        instructions = [line.strip() for line in f.readlines()]

    head, tail = Point2D(0, 0), Point2D(0, 0)
    tail_history = {tail}
    for instruction in instructions:
        direction, count = instruction.split(" ")
        for _ in range(int(count)):
            t = head
            head = head + DIRECTION_MAPPING[direction]
            if not tail.touching(head):
                tail = t
                tail_history.add(tail)
    return len(tail_history)


def get_delta(p1: Point2D, p2: Point2D) -> Point2D:
    if p1.touching(p2):
        return Point2D(0, 0)
    return Point2D(
        (p2.x - p1.x) // (abs(p2.x - p1.x) or 1),
        (p2.y - p1.y) // (abs(p2.y - p1.y) or 1),
    )


def part_2(file_path: str) -> int:
    with open(file_path) as f:
        instructions = [line.strip() for line in f.readlines()]

    rope = [Point2D(0, 0) for _ in range(10)]
    tail_history = {rope[-1]}
    for instruction in instructions:
        direction, count = instruction.split(" ")
        for _ in range(int(count)):
            next_rope = [rope[0] + DIRECTION_MAPPING[direction]]
            for idx in range(1, 10):
                delta = get_delta(rope[idx], next_rope[idx - 1])
                next_rope.append(rope[idx] + delta)
            rope = next_rope
            tail_history.add(rope[-1])
    return len(tail_history)
