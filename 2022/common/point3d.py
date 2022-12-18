from __future__ import annotations

import dataclasses


@dataclasses.dataclass(frozen=True)
class Point3D:
    x: int
    y: int
    z: int

    def __add__(self, other: Point3D) -> Point3D:
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Point3D) -> Point3D:
        return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, f: int) -> Point3D:
        return Point3D(self.x * f, self.y * f, self.z * f)

    def taxicab(self, other: Point3D) -> int:
        p = self - other
        return abs(p.x) + abs(p.y) + abs(p.z)


@dataclasses.dataclass(frozen=True)
class Box3D:
    bottom_left: Point3D
    top_right: Point3D

    def __post_init__(self):
        assert self.bottom_left.x <= self.top_right.x
        assert self.bottom_left.y <= self.top_right.y
        assert self.bottom_left.z <= self.top_right.z

    @property
    def points(self) -> set[Point3D]:
        return set(
            Point3D(x, y, z)
            for x in range(self.bottom_left.x, self.top_right.x + 1)
            for y in range(self.bottom_left.y, self.top_right.y + 1)
            for z in range(self.bottom_left.z, self.top_right.z + 1)
        )

    def contains(self, p: Point3D) -> bool:
        return (
            self.bottom_left.x <= p.x <= self.top_right.x
            and self.bottom_left.y <= p.y <= self.top_right.y
            and self.bottom_left.z <= p.z <= self.top_right.z
        )
