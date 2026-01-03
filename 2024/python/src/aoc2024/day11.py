import functools
from pathlib import Path


def part_1(input: Path) -> int:
    stones = list(map(int, input.read_text().strip().split()))
    return sum(count_stones(stone, 25) for stone in stones)


def part_2(input: Path) -> int:
    stones = list(map(int, input.read_text().strip().split()))
    return sum(count_stones(stone, 75) for stone in stones)


@functools.cache
def count_stones(stone: int, blinks_remaining: int) -> int:
    if blinks_remaining == 0:
        return 1

    if stone == 0:
        return count_stones(1, blinks_remaining - 1)

    str_stone = str(stone)
    if len(str_stone) % 2 == 0:
        return count_stones(
            int(str_stone[: len(str_stone) // 2]),
            blinks_remaining - 1,
        ) + count_stones(
            int(str_stone[len(str_stone) // 2 :]),
            blinks_remaining - 1,
        )

    return count_stones(stone * 2024, blinks_remaining - 1)
