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
