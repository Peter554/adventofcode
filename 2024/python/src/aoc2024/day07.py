from pathlib import Path


def part_1(input: Path) -> int:
    equations = []
    for line in input.read_text().splitlines():
        target = int(line.split(":")[0])
        numbers = list(map(int, line.split(":")[1].strip().split()))
        equations.append((target, numbers))

    return sum(
        target
        for target, numbers in equations
        if count_solutions(target, numbers, with_concatenation=False) > 0
    )


def part_2(input: Path) -> int:
    equations = []
    for line in input.read_text().splitlines():
        target = int(line.split(":")[0])
        numbers = list(map(int, line.split(":")[1].strip().split()))
        equations.append((target, numbers))

    return sum(
        target
        for target, numbers in equations
        if count_solutions(target, numbers, with_concatenation=True) > 0
    )


def count_solutions(
    target: int, numbers: list[int], *, with_concatenation: bool
) -> int:
    if len(numbers) == 1:
        return 1 if numbers[0] == target else 0

    count = 0

    # Operator: +
    if target - numbers[-1] >= 0:
        count += count_solutions(
            target - numbers[-1],
            numbers[:-1],
            with_concatenation=with_concatenation,
        )

    # Operator: *
    if target % numbers[-1] == 0:
        count += count_solutions(
            target // numbers[-1],
            numbers[:-1],
            with_concatenation=with_concatenation,
        )

    # Operator: ||
    if (
        with_concatenation
        and target > numbers[-1]
        and str(target).endswith(str(numbers[-1]))
    ):
        count += count_solutions(
            int(str(target).removesuffix(str(numbers[-1]))),
            numbers[:-1],
            with_concatenation=with_concatenation,
        )

    return count
