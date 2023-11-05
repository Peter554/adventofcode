def part_1(file_path: str) -> int:
    with open(file_path, "r") as f:
        numbers = [int(line) for line in f]
    return sum([numbers[i] < numbers[i + 1] for i in range(len(numbers) - 1)])


def part_2(file_path: str) -> int:
    with open(file_path, "r") as f:
        numbers = [int(line) for line in f]
    numbers = [sum(numbers[i : i + 3]) for i in range(len(numbers) - 2)]
    return sum([numbers[i] < numbers[i + 1] for i in range(len(numbers) - 1)])
