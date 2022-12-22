from __future__ import annotations

import enum
import re

from common.point2d import Point2D

ROUTE_PATH = "day22/route"
MAPS_PATH = "day22/maps"


class Turn(enum.Enum):
    LEFT = enum.auto()
    RIGHT = enum.auto()


Route = list[int | Turn]


def parse_route() -> Route:
    with open(ROUTE_PATH) as f:
        s = f.readline().strip()
    route: Route = []
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


Map = set[Point2D]
Maps = dict[int, Map]


def parse_maps() -> Maps:
    with open(MAPS_PATH) as f:
        raw_maps = f.read().split("\n\n")
    maps: Maps = {}
    for idx, raw_map in enumerate(raw_maps):
        map_: Map = set()
        for y, line in enumerate(raw_map.split()):
            for x, char in enumerate(line.strip()):
                if char == "#":
                    continue
                map_.add(Point2D(x, y))
        maps[idx] = map_
    return maps


class Direction(enum.Enum):
    RIGHT = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    UP = enum.auto()


class Simulation:
    def __init__(self, route: Route, maps: Maps):
        self.route = route
        self.maps = maps
        self.map_idx = 0
        self.position = Point2D(0, 0)
        self.direction = Direction.RIGHT

    @property
    def map(self) -> Map:
        return self.maps[self.map_idx]

    def execute(self):
        for instruction in self.route:
            if isinstance(instruction, Turn):
                self.turn(instruction)
            else:
                for _ in range(instruction):
                    self.step()

    def turn(self, turn: Turn):
        if turn == Turn.LEFT:
            self.direction = {
                Direction.RIGHT: Direction.UP,
                Direction.DOWN: Direction.RIGHT,
                Direction.LEFT: Direction.DOWN,
                Direction.UP: Direction.LEFT,
            }[self.direction]
        self.direction = {
            Direction.RIGHT: Direction.DOWN,
            Direction.DOWN: Direction.LEFT,
            Direction.LEFT: Direction.UP,
            Direction.UP: Direction.RIGHT,
        }[self.direction]

    def step(self):
        ...


def score(map_idx: int, position: Point2D, direction: Direction) -> int:
    x_offset = {
        0: 50,
        1: 100,
        2: 50,
        3: 0,
        4: 50,
        5: 0,
    }[map_idx]
    y_offset = {
        0: 0,
        1: 0,
        2: 50,
        3: 100,
        4: 100,
        5: 150,
    }[map_idx]
    direction_score = {
        Direction.RIGHT: 0,
        Direction.DOWN: 1,
        Direction.LEFT: 2,
        Direction.UP: 3,
    }[direction]
    return (
        1000 * (position.x + x_offset + 1)
        + 4 * (position.y + y_offset + 1)
        + direction_score
    )


def part_1() -> int:
    route = parse_route()
    maps = parse_maps()
    simulation = Simulation(route, maps)
    simulation.execute()
    return score(simulation.map_idx, simulation.position, simulation.direction)


def part_2() -> int:
    return 1
