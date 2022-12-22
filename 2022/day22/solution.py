from __future__ import annotations

import enum
import re

from common.point2d import Point2D

ROUTE_PATH = "day22/route"
MAPS_PATH = "day22/maps"


class Turn(enum.Enum):
    LEFT = enum.auto()
    RIGHT = enum.auto()


def parse_route() -> list[int | Turn]:
    with open(ROUTE_PATH) as f:
        s = f.readline().strip()
    route: list[int | Turn] = []
    while s:
        if s.startswith("L"):
            route.append(Turn.LEFT)
            s = s[1:]
        elif s.startswith("R"):
            route.append(Turn.RIGHT)
            s = s[1:]
        else:
            match = re.match(r"^(\d+)(?:L|R|$)", s)
            assert match is not None
            t = match.group(1)
            route.append(int(t))
            s = s[len(t) :]
    return route


def parse_maps() -> dict[int, set[Point2D]]:
    with open(MAPS_PATH) as f:
        raw_maps = f.read().split("\n\n")
    maps: dict[int, set[Point2D]] = {}
    for idx, raw_map in enumerate(raw_maps):
        map_: set[Point2D] = set()
        for y, line in enumerate(raw_map.split()):
            for x, char in enumerate(line.strip()):
                if char == "#":
                    continue
                map_.add(Point2D(x, y))
        maps[idx] = map_
    return maps


def part_1() -> int:
    return 1


def part_2() -> int:
    return 1
