import enum
from typing import Protocol

from common.point2d import Point2D


class Direction(enum.Enum):
    RIGHT = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    UP = enum.auto()


class SwitchMap(Protocol):
    def __call__(
        self, map_size: int, map_idx: int, position: Point2D, direction: Direction
    ) -> tuple[int, Point2D, Direction]:
        ...
