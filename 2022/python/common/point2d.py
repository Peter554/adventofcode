from __future__ import annotations

import dataclasses


@dataclasses.dataclass(frozen=True)
class Point2D:
    x: int
    y: int

    def __add__(self, other: Point2D) -> Point2D:
        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point2D) -> Point2D:
        return Point2D(self.x - other.x, self.y - other.y)

    def __mul__(self, f: int) -> Point2D:
        return Point2D(self.x * f, self.y * f)

    def taxicab(self, other: Point2D) -> int:
        p = self - other
        return abs(p.x) + abs(p.y)


@dataclasses.dataclass(frozen=True)
class Box2D:
    bottom_left: Point2D
    top_right: Point2D

    def __post_init__(self):
        assert self.bottom_left.x <= self.top_right.x
        assert self.bottom_left.y <= self.top_right.y

    @property
    def points(self) -> set[Point2D]:
        return set(
            Point2D(x, y)
            for x in range(self.bottom_left.x, self.top_right.x + 1)
            for y in range(self.bottom_left.y, self.top_right.y + 1)
        )

    def contains(self, p: Point2D) -> bool:
        return (
            self.bottom_left.x <= p.x <= self.top_right.x
            and self.bottom_left.y <= p.y <= self.top_right.y
        )
