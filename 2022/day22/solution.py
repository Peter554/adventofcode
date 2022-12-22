from __future__ import annotations

import enum
import re

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


def part_1() -> int:
    return 1


def part_2() -> int:
    return 1
