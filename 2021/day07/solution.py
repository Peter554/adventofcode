import math
import statistics


def part_1(file_path: str) -> int:
    with open(file_path, "r") as f:
        crab_positions = [int(n) for n in f.readline().split(",")]

    def cost(position: int) -> int:
        return sum([abs(p - position) for p in crab_positions])

    optimal_position = math.floor(statistics.median(crab_positions))
    return cost(optimal_position)


def part_2(file_path: str) -> int:
    with open(file_path, "r") as f:
        crab_positions = [int(n) for n in f.readline().split(",")]

    def cost(position: int) -> int:
        return sum(
            [
                int(0.5 * abs(p - position) * (abs(p - position) + 1))
                for p in crab_positions
            ]
        )

    lower_p, higher_p = min(crab_positions), max(crab_positions)
    while True:
        test_p = math.floor(0.5 * (lower_p + higher_p))
        if test_p == lower_p:
            return min([cost(lower_p), cost(higher_p)])
        if cost(test_p) < cost(test_p - 1) and cost(test_p) < cost(test_p + 1):
            return cost(test_p)
        elif cost(test_p) < cost(test_p + 1):
            higher_p = test_p
        else:
            lower_p = test_p
