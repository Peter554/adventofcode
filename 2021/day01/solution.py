def part_1(file_path) -> int:
    with open(file_path, "r") as f:
        numbers = [int(line) for line in f]
    return sum([numbers[i] > numbers[i - 1] for i in range(1, len(numbers))])


def part_2(file_path) -> int:
    with open(file_path, "r") as f:
        numbers = [int(line) for line in f]
    numbers = [
        numbers[i] + numbers[i - 1] + numbers[i - 2] for i in range(2, len(numbers))
    ]
    return sum([numbers[i] > numbers[i - 1] for i in range(1, len(numbers))])
