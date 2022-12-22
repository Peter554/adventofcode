from __future__ import annotations

import os
import enum
import re
import importlib

from day22.base import Point2D, Direction, SwitchMap


class Turn(enum.Enum):
    LEFT = enum.auto()
    RIGHT = enum.auto()


Route = list[int | Turn]


def parse_route(file_path: str) -> Route:
    with open(file_path) as f:
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


def parse_maps(file_path: str) -> tuple[int, Maps]:
    with open(file_path) as f:
        raw_maps = f.read().split("\n\n")
    map_size = 0
    maps: Maps = {}
    for idx, raw_map in enumerate(raw_maps):
        map_: Map = set()
        for y, line in enumerate(raw_map.split()):
            map_size = len(line.strip())
            for x, char in enumerate(line.strip()):
                if char == "#":
                    continue
                map_.add(Point2D(x, y))
        maps[idx] = map_
    return map_size, maps


class Simulation:
    def __init__(self, route: Route, map_size: int, maps: Maps, switch_map: SwitchMap):
        self.route = route
        self.map_size = map_size
        self.maps = maps
        self.switch_map = switch_map
        #
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
        else:
            self.direction = {
                Direction.RIGHT: Direction.DOWN,
                Direction.DOWN: Direction.LEFT,
                Direction.LEFT: Direction.UP,
                Direction.UP: Direction.RIGHT,
            }[self.direction]

    def step(self):
        delta = {
            Direction.RIGHT: Point2D(1, 0),
            Direction.DOWN: Point2D(0, 1),
            Direction.LEFT: Point2D(-1, 0),
            Direction.UP: Point2D(0, -1),
        }[self.direction]
        next_position = self.position + delta
        if (
            next_position.x < 0
            or next_position.x > self.map_size - 1
            or next_position.y < 0
            or next_position.y > self.map_size - 1
        ):
            next_map_idx, next_position, next_direction = self.switch_map(
                self.map_size, self.map_idx, self.position, self.direction
            )
            if next_position not in self.maps[next_map_idx]:
                return
            self.map_idx = next_map_idx
            self.position = next_position
            self.direction = next_direction
        elif next_position in self.map:
            self.position = next_position


def score(
    map_idx: int,
    position: Point2D,
    direction: Direction,
    x_offsets: dict[int, int],
    y_offsets: dict[int, int],
) -> int:
    x_offset = x_offsets[map_idx]
    y_offset = y_offsets[map_idx]
    direction_score = {
        Direction.RIGHT: 0,
        Direction.DOWN: 1,
        Direction.LEFT: 2,
        Direction.UP: 3,
    }[direction]
    return (
        1000 * (position.y + y_offset + 1)
        + 4 * (position.x + x_offset + 1)
        + direction_score
    )


def part_1(file_path: str) -> int:
    route = parse_route(os.path.join(file_path, "route"))
    map_size, maps = parse_maps(os.path.join(file_path, "maps"))
    logic = importlib.import_module(file_path.replace("/", ".") + ".logic")

    simulation = Simulation(route, map_size, maps, logic.switch_map_v1)
    simulation.execute()

    return score(
        simulation.map_idx,
        simulation.position,
        simulation.direction,
        logic.X_OFFSETS,
        logic.Y_OFFSETS,
    )


def part_2(file_path: str) -> int:
    return 1
