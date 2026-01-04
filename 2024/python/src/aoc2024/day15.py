from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


def part_1(input: Path) -> int:
    robot: P | None = None
    walls: set[P] = set()
    boxes: set[P] = set()
    for y, line in enumerate(input.read_text().split("\n\n")[0].splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                walls.add(P(x, y))
            elif c == "@":
                robot = P(x, y)
            elif c == "O":
                boxes.add(P(x, y))
    assert robot is not None

    moves = "".join(input.read_text().split("\n\n")[1].splitlines())

    for move in moves:
        match move:
            case "^":
                delta = P(0, -1)
            case "v":
                delta = P(0, 1)
            case "<":
                delta = P(-1, 0)
            case ">":
                delta = P(1, 0)
            case _:
                raise ValueError(f"Invalid move: {move}")

        p = robot + delta
        while p in boxes:
            p += delta

        if p in walls:
            # Move failed
            continue
        else:
            robot += delta
            if robot in boxes:
                boxes.remove(robot)
                boxes.add(p)

    return sum(100 * b.y + b.x for b in boxes)


@dataclass(frozen=True)
class P:
    x: int
    y: int

    def __add__(self, other: P) -> P:
        return P(self.x + other.x, self.y + other.y)
