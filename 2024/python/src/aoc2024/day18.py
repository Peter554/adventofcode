from __future__ import annotations

import heapq
import itertools
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class P:
    x: int
    y: int

    def __add__(self, other) -> P:
        return P(self.x + other.x, self.y + other.y)


UP = P(0, -1)
DOWN = P(0, 1)
LEFT = P(-1, 0)
RIGHT = P(1, 0)


def part_1(input: Path, memory_space_size: int, n_bytes_to_drop: int) -> int:
    corrupt_memory = frozenset(
        [P(*map(int, line.split(","))) for line in input.read_text().splitlines()][
            :n_bytes_to_drop
        ]
    )
    path_len = _find_path_len(memory_space_size, corrupt_memory)
    assert path_len is not None, "no solution"
    return path_len


def part_2(input: Path, memory_space_size: int) -> tuple[int, int]:
    bytes_to_drop = [
        P(*map(int, line.split(","))) for line in input.read_text().splitlines()
    ]

    def find_path_len(i: int) -> int | None:
        corrupt_memory = frozenset(bytes_to_drop[: i + 1])
        return _find_path_len(memory_space_size, corrupt_memory)

    low, high = 0, len(bytes_to_drop) - 1
    while low < high:
        mid = (low + high) // 2
        if find_path_len(mid) is None:
            high = mid
        else:
            low = mid + 1

    return bytes_to_drop[low].x, bytes_to_drop[low].y


def _find_path_len(memory_space_size: int, corrupt_memory: frozenset[P]) -> int | None:
    start = P(0, 0)
    goal = P(memory_space_size, memory_space_size)

    counter = itertools.count()  # For tie-breaking
    q = [(0, next(counter), start)]
    shortest_paths = {}
    while q:
        path_len, _, p = heapq.heappop(q)
        if p in shortest_paths and path_len >= shortest_paths[p]:
            continue

        shortest_paths[p] = path_len

        for direction in [UP, DOWN, LEFT, RIGHT]:
            neighbor = p + direction
            if not _is_in_bounds(neighbor, memory_space_size):
                continue
            if neighbor in corrupt_memory:
                continue
            heapq.heappush(q, (path_len + 1, next(counter), neighbor))

    return shortest_paths.get(goal, None)


def _is_in_bounds(p: P, memory_space_size: int) -> bool:
    return 0 <= p.x <= memory_space_size and 0 <= p.y <= memory_space_size
