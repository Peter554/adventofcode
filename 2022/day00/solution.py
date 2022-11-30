# 2021 day 1


def part_1(lines: list[str]) -> int:
    numbers = [int(line) for line in lines]
    return sum(numbers[i + 1] > numbers[i] for i in range(len(numbers) - 1))


def part_2(lines: list[str]) -> int:
    numbers = [int(line) for line in lines]
    sums = [sum(numbers[i : i + 3]) for i in range(len(numbers) - 2)]
    return sum(sums[i + 1] > sums[i] for i in range(len(sums) - 1))
