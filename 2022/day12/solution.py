from common.point2d import Point2D
from common.shortest_path import find_shortest_paths


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

    def get_state_transitions(state: Point2D):
        return tuple(
            (1, state + delta)
            for delta in [Point2D(1, 0), Point2D(-1, 0), Point2D(0, 1), Point2D(0, -1)]
            if state + delta in terrain and terrain[state + delta] <= terrain[state] + 1
        )

    shortest_paths = find_shortest_paths(origin, get_state_transitions)
    return shortest_paths[destination].cost


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

    def get_state_transitions(state: Point2D):
        return tuple(
            (1, state + delta)
            for delta in [Point2D(1, 0), Point2D(-1, 0), Point2D(0, 1), Point2D(0, -1)]
            if state + delta in terrain and terrain[state + delta] >= terrain[state] - 1
        )

    shortest_paths = find_shortest_paths(destination, get_state_transitions)
    return min(
        shortest_paths[origin].cost for origin in origins if origin in shortest_paths
    )
