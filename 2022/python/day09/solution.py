import time
from typing import Literal
import argparse

from rich.live import Live
from rich.text import Text

from common.point2d import Point2D


def touching(p1: Point2D, p2: Point2D) -> bool:
    return max(abs(p1.x - p2.x), abs(p1.y - p2.y)) <= 1


Direction = Literal["U", "D", "L", "R"]


def parse_direction(s: str) -> Direction:
    mapping: dict[str, Direction] = {"U": "U", "D": "D", "L": "L", "R": "R"}
    return mapping[s]


class Rope:
    _DIRECTION_DELTA_MAPPING: dict[Direction, Point2D] = {
        "U": Point2D(0, 1),
        "D": Point2D(0, -1),
        "L": Point2D(-1, 0),
        "R": Point2D(1, 0),
    }

    def __init__(self, length: int):
        self._state = [Point2D(0, 0) for _ in range(length)]

    @property
    def state(self) -> tuple[Point2D, ...]:
        return tuple(self._state)

    def evolve(self, direction: Direction) -> None:
        next_state = [self._state[0] + self._DIRECTION_DELTA_MAPPING[direction]]
        for idx in range(1, len(self._state)):
            delta = self._get_delta(self._state[idx], next_state[idx - 1])
            next_state.append(self._state[idx] + delta)
        self._state = next_state

    @staticmethod
    def _get_delta(tail: Point2D, head: Point2D) -> Point2D:
        if touching(tail, head):
            return Point2D(0, 0)
        # same row/column: move horizontal
        # else: move diagonal
        return Point2D(
            (head.x - tail.x) // (abs(head.x - tail.x) or 1),
            (head.y - tail.y) // (abs(head.y - tail.y) or 1),
        )


def solve_puzzle(file_path: str, rope_length: int) -> int:
    with open(file_path) as f:
        instructions = [line.strip() for line in f.readlines()]
    rope = Rope(rope_length)
    rope_tail_history = {rope.state[-1]}
    for instruction in instructions:
        direction, count = instruction.split(" ")
        for _ in range(int(count)):
            rope.evolve(parse_direction(direction))
            rope_tail_history.add(rope.state[-1])
    return len(rope_tail_history)


def part_1(file_path: str) -> int:
    return solve_puzzle(file_path, 2)


def part_2(file_path: str) -> int:
    return solve_puzzle(file_path, 10)


def render_rope_state(
    rope_state: tuple[Point2D, ...], render_box: tuple[Point2D, Point2D]
):
    bottom_left, top_right = render_box
    s = ""
    for y in range(top_right.y, bottom_left.y - 1, -1):
        for x in range(bottom_left.x, top_right.x + 1):
            p = Point2D(x, y)
            if p in rope_state:
                if p == rope_state[0]:
                    s += "H"
                elif p == rope_state[-1]:
                    s += "T"
                else:
                    s += "#"
            else:
                s += "."
        s += "\n"
    return Text(s)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--file", default="day09/sample2")
    arg_parser.add_argument("--xmax", type=int, default=20)
    arg_parser.add_argument("--ymax", type=int, default=20)
    arg_parser.add_argument("--dt", type=float, default=0.2)
    args = arg_parser.parse_args()

    with open(args.file) as f:
        instructions = [line.strip() for line in f.readlines()]

    rope = Rope(10)
    render_box = (Point2D(-args.xmax, -args.ymax), Point2D(args.xmax, args.ymax))
    with Live(render_rope_state(rope.state, render_box), auto_refresh=False) as live:
        for instruction in instructions:
            direction, count = instruction.split(" ")
            for _ in range(int(count)):
                time.sleep(args.dt)
                rope.evolve(parse_direction(direction))
                live.update(render_rope_state(rope.state, render_box))
                live.refresh()
