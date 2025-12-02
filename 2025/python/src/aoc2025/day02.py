from pathlib import Path


def part_1(input: Path) -> int:
    ranges = parse_ranges(input)
    sum_invalid_ids = 0
    i = 1
    while (n := int(f"{i}{i}")) <= ranges[-1][1]:
        if is_in_ranges(n, ranges):
            sum_invalid_ids += n
        i += 1
    return sum_invalid_ids


def part_2(input: Path) -> int:
    ranges = parse_ranges(input)
    invalid_ids = set()
    i = 1
    while int(f"{i}{i}") <= ranges[-1][1]:
        j = 2
        while (n := int(f"{i}" * j)) <= ranges[-1][1]:
            if is_in_ranges(n, ranges):
                invalid_ids.add(n)
            j += 1
        i += 1
    return sum(invalid_ids)


def parse_ranges(input: Path) -> tuple[tuple[int, int], ...]:
    return tuple(
        sorted(
            (int(raw_range.split("-")[0]), int(raw_range.split("-")[1]))
            for raw_range in input.read_text().strip().split(",")
        )
    )


def is_in_ranges(n: int, ranges: tuple[tuple[int, int], ...]) -> bool:
    for range in ranges:
        if range[0] <= n <= range[1]:
            return True
    return False
