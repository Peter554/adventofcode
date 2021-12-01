# 2020 day 1
def part_1(file_path) -> int:
    with open(file_path, "r") as f:
        numbers = [int(line) for line in f.readlines()]
    for i, n in enumerate(numbers):
        for j, m in enumerate(numbers):
            if i == j:
                continue
            if n + m == 2020:
                return n * m
    raise Exception("no solution found")
