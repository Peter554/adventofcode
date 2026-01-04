import re
import statistics
from pathlib import Path


def part_1(input: Path, width: int, height: int) -> int:
    top_left_robots = 0
    bottom_left_robots = 0
    top_right_robots = 0
    bottom_right_robots = 0

    for line in input.read_text().splitlines():
        match = re.search(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", line)
        assert match is not None
        px = int(match.group(1))
        py = int(match.group(2))
        vx = int(match.group(3))
        vy = int(match.group(4))

        px = (px + vx * 100) % width
        py = (py + vy * 100) % height
        if px < width // 2:
            if py < height // 2:
                top_left_robots += 1
            elif py > height // 2:
                bottom_left_robots += 1
        elif px > width // 2:
            if py < height // 2:
                top_right_robots += 1
            elif py > height // 2:
                bottom_right_robots += 1

    return top_left_robots * bottom_left_robots * top_right_robots * bottom_right_robots


def part_2(input: Path, width: int, height: int) -> int:
    xs = []
    ys = []
    vxs = []
    vys = []
    for line in input.read_text().splitlines():
        match = re.search(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", line)
        assert match is not None
        xs.append(int(match.group(1)))
        ys.append(int(match.group(2)))
        vxs.append(int(match.group(3)))
        vys.append(int(match.group(4)))

    xmas_time = -1
    min_variance = statistics.variance(xs) + statistics.variance(ys)
    for t in range(1, width * height):
        # We're guaranteed to cycle after width * height timesteps.
        for i in range(len(xs)):
            xs[i] = (xs[i] + vxs[i]) % width
            ys[i] = (ys[i] + vys[i]) % height
        variance = statistics.variance(xs) + statistics.variance(ys)
        if variance < min_variance:
            min_variance = variance
            # Assumption: xmas tree configuration will have lowest variance.
            xmas_time = t

    return xmas_time
