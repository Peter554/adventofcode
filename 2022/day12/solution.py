from __future__ import annotations

import dataclasses
import heapq


@dataclasses.dataclass(frozen=True)
class Point2D:
    x: int
    y: int

    def __add__(self, other: Point2D) -> Point2D:
        return Point2D(self.x + other.x, self.y + other.y)


def part_1(file_path: str) -> int:
    with open(file_path) as f:
        raw_data = {
            Point2D(x, y): char
            for y, line in enumerate(f.readlines())
            for x, char in enumerate(line.strip())
        }

    origin = [k for k, v in raw_data.items() if v == "S"][0]
    destination = [k for k, v in raw_data.items() if v == "E"][0]
    raw_data[origin] = "a"
    raw_data[destination] = "z"
    terrain = {k: ord(v) - ord("a") for k, v in raw_data.items()}

    def get_neighbors(point: Point2D):
        return tuple(
            (point + delta, 1)
            for delta in [
                Point2D(1, 0),
                Point2D(-1, 0),
                Point2D(0, 1),
                Point2D(0, -1),
            ]
            if point + delta in terrain and terrain[point + delta] <= terrain[point] + 1
        )

    shortest_paths: dict[Point2D, int] = {}
    to_visit: list[tuple[int, int, Point2D]] = []  # heapq
    tie_break = 0  # in case of equal cost
    heapq.heappush(to_visit, (0, tie_break, origin))
    while to_visit:
        cost, _, point = heapq.heappop(to_visit)
        if point in shortest_paths and shortest_paths[point] <= cost:
            continue
        shortest_paths[point] = cost
        for neighbor, delta_cost in get_neighbors(point):
            tie_break += 1
            heapq.heappush(to_visit, (cost + delta_cost, tie_break, neighbor))

    return shortest_paths[destination]


def part_2(file_path: str) -> int:
    with open(file_path) as f:
        raw_data = {
            Point2D(x, y): char
            for y, line in enumerate(f.readlines())
            for x, char in enumerate(line.strip())
        }

    original_origin = [k for k, v in raw_data.items() if v == "S"][0]
    origins = [k for k, v in raw_data.items() if v == "S" or v == "a"]
    destination = [k for k, v in raw_data.items() if v == "E"][0]
    raw_data[original_origin] = "a"
    raw_data[destination] = "z"
    terrain = {k: ord(v) - ord("a") for k, v in raw_data.items()}

    def get_neighbors(point: Point2D):
        return tuple(
            (point + delta, 1)
            for delta in [
                Point2D(1, 0),
                Point2D(-1, 0),
                Point2D(0, 1),
                Point2D(0, -1),
            ]
            if point + delta in terrain and terrain[point + delta] >= terrain[point] - 1
        )

    shortest_paths: dict[Point2D, int] = {}
    to_visit: list[tuple[int, int, Point2D]] = []  # heapq
    tie_break = 0  # in case of equal cost
    heapq.heappush(to_visit, (0, tie_break, destination))
    while to_visit:
        cost, _, point = heapq.heappop(to_visit)
        if point in shortest_paths and shortest_paths[point] <= cost:
            continue
        shortest_paths[point] = cost
        for neighbor, delta_cost in get_neighbors(point):
            tie_break += 1
            heapq.heappush(to_visit, (cost + delta_cost, tie_break, neighbor))

    return min(shortest_paths[origin] for origin in origins if origin in shortest_paths)
