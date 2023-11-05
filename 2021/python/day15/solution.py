import heapq
import itertools


def neighbourhood(p: tuple[int, int]) -> set[tuple[int, int]]:
    i, j = p
    return {
        (i - 1, j),
        (i + 1, j),
        (i, j - 1),
        (i, j + 1),
    }


def part_1(file_path: str) -> int:
    with open(file_path, "r") as f:
        lines = f.read().splitlines()

    entry_costs = {}
    for i, line in enumerate(lines):
        for j, cost_str in enumerate(list(line)):
            entry_costs[(i, j)] = int(cost_str)

    i_max = max([i for (i, _) in entry_costs])
    j_max = max([j for (_, j) in entry_costs])

    path_costs = {(0, 0): 0}
    q = [(0, (0, 0))]
    heapq.heapify(q)
    while (i_max, j_max) not in path_costs:
        _, p = heapq.heappop(q)
        for neighbour in neighbourhood(p):
            if neighbour not in entry_costs or neighbour in path_costs:
                continue
            neighbour_cost = path_costs[p] + entry_costs[neighbour]
            path_costs[neighbour] = neighbour_cost
            heapq.heappush(q, (neighbour_cost, neighbour))

    return path_costs[(i_max, j_max)]


def part_2(file_path: str) -> int:
    with open(file_path, "r") as f:
        lines = f.read().splitlines()

    entry_costs = {}
    for i, line in enumerate(lines):
        for j, cost_str in enumerate(list(line)):
            entry_costs[(i, j)] = int(cost_str)

    i_max = max([i for (i, _) in entry_costs])
    j_max = max([j for (_, j) in entry_costs])

    for i_factor, j_factor in itertools.product(range(5), range(5)):
        if (i_factor, j_factor) == (0, 0):
            continue
        for (i, j) in itertools.product(range(i_max + 1), range(j_max + 1)):
            point = ((i_max + 1) * i_factor + i, (j_max + 1) * j_factor + j)
            cost = entry_costs[(i, j)] + i_factor + j_factor
            if cost > 9:
                cost = cost % 9
            entry_costs[point] = cost

    i_max = max([i for (i, _) in entry_costs])
    j_max = max([j for (_, j) in entry_costs])

    path_costs = {(0, 0): 0}
    q = [(0, (0, 0))]
    heapq.heapify(q)
    while (i_max, j_max) not in path_costs:
        _, p = heapq.heappop(q)
        for neighbour in neighbourhood(p):
            if neighbour not in entry_costs or neighbour in path_costs:
                continue
            neighbour_cost = path_costs[p] + entry_costs[neighbour]
            path_costs[neighbour] = neighbour_cost
            heapq.heappush(q, (neighbour_cost, neighbour))

    return path_costs[(i_max, j_max)]
