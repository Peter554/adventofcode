import itertools


def part_1(file_path: str) -> int:
    with open(file_path, "r") as f:
        lines = f.read().splitlines()

    states = {}
    for i, line in enumerate(lines):
        for j, energy in enumerate(line):
            states[(i, j)] = int(energy)

    flashes = 0
    for _ in range(100):
        states = {k: v + 1 for k, v in states.items()}
        flashing = {k for k, v in states.items() if v >= 10}
        flashed: set[tuple[int, int]] = set()
        while flashing:
            for k in [*flashing]:
                for i, j in itertools.product(
                    range(k[0] - 1, k[0] + 2), range(k[1] - 1, k[1] + 2)
                ):
                    if (i, j) == k or (i, j) not in states:
                        continue
                    states[(i, j)] += 1
                flashing.remove(k)
                flashed.add(k)
            flashing = {k for k, v in states.items() if v >= 10 and k not in flashed}
        flashes += len(flashed)
        for k in flashed:
            states[k] = 0
    return flashes


def part_2(file_path: str) -> int:
    with open(file_path, "r") as f:
        lines = f.read().splitlines()

    states = {}
    for i, line in enumerate(lines):
        for j, energy in enumerate(line):
            states[(i, j)] = int(energy)

    iteration = 0
    while True:
        iteration += 1
        states = {k: v + 1 for k, v in states.items()}
        flashing = {k for k, v in states.items() if v >= 10}
        flashed: set[tuple[int, int]] = set()
        while flashing:
            for k in [*flashing]:
                for i, j in itertools.product(
                    range(k[0] - 1, k[0] + 2), range(k[1] - 1, k[1] + 2)
                ):
                    if (i, j) == k or (i, j) not in states:
                        continue
                    states[(i, j)] += 1
                flashing.remove(k)
                flashed.add(k)
            flashing = {k for k, v in states.items() if v >= 10 and k not in flashed}
        for k in flashed:
            states[k] = 0
        if len(flashed) == len(states):
            return iteration
