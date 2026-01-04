from __future__ import annotations

import collections
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


def part_2(input: Path) -> int:
    robot: P | None = None
    walls: set[P] = set()
    boxes: set[P] = set()  # Left side of box
    for y, line in enumerate(input.read_text().split("\n\n")[0].splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                walls.add(P(2 * x, y))
                walls.add(P(2 * x + 1, y))
            elif c == "@":
                robot = P(2 * x, y)
            elif c == "O":
                boxes.add(P(2 * x, y))
    assert robot is not None

    walls_by_y: dict[int, set[P]] = collections.defaultdict(set)
    for wall in walls:
        walls_by_y[wall.y].add(wall)
    boxes_by_y: dict[int, set[P]] = collections.defaultdict(set)
    for box in boxes:
        boxes_by_y[box.y].add(box)

    moves = "".join(input.read_text().split("\n\n")[1].splitlines())

    for move in moves:
        if move in {"<", ">"}:
            dx = 1 if move == ">" else -1

            p = robot + P(dx, 0)
            boxes_to_move = set()
            while p in boxes or p + P(-1, 0) in boxes:
                if p in boxes:
                    boxes_to_move.add(p)
                p += P(dx, 0)

            if p in walls:
                # Move failed
                continue
            else:
                robot += P(dx, 0)
                for box in boxes_to_move:
                    boxes.remove(box)
                    boxes_by_y[box.y].remove(box)
                for box in boxes_to_move:
                    boxes.add(box + P(dx, 0))
                    boxes_by_y[box.y].add(box + P(dx, 0))

        elif move in {"^", "v"}:
            dy = 1 if move == "v" else -1

            move_ok = True
            boxes_to_move = set()
            xs = {robot.x}
            y = robot.y
            while True:
                y += dy

                walls_hit_at_y = {w for w in walls_by_y[y] if w.x in xs}
                if walls_hit_at_y:
                    move_ok = False
                    break

                boxes_to_move_at_y = {
                    b for b in boxes_by_y[y] if b.x in xs or b.x + 1 in xs
                }
                boxes_to_move |= boxes_to_move_at_y

                if not boxes_to_move_at_y:
                    break

                xs = {b.x for b in boxes_to_move_at_y} | {
                    b.x + 1 for b in boxes_to_move_at_y
                }

            if move_ok:
                robot += P(0, dy)
                for box in boxes_to_move:
                    boxes.remove(box)
                    boxes_by_y[box.y].remove(box)
                for box in boxes_to_move:
                    boxes.add(box + P(0, dy))
                    boxes_by_y[box.y + dy].add(box + P(0, dy))

    return sum(100 * b.y + b.x for b in boxes)


@dataclass(frozen=True)
class P:
    x: int
    y: int

    def __add__(self, other: P) -> P:
        return P(self.x + other.x, self.y + other.y)

    def __mul__(self, other: int) -> P:
        return P(self.x * other, self.y * other)
