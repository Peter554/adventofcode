import functools
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


def part_1(input_path: Path) -> int:
    parsed = _parse(input_path)
    count_possibilities = _get_count_possibilities(parsed.towels)
    return sum(bool(count_possibilities(design)) for design in parsed.designs)


def part_2(input_path: Path) -> int:
    parsed = _parse(input_path)
    count_possibilities = _get_count_possibilities(parsed.towels)
    return sum(count_possibilities(design) for design in parsed.designs)


@dataclass
class _Puzzle:
    towels: list[str]
    designs: list[str]


def _parse(input_path: Path) -> _Puzzle:
    parts = input_path.read_text().split("\n\n")
    towels = [s.strip() for s in parts[0].split(",")]
    designs = parts[1].splitlines()
    return _Puzzle(towels=towels, designs=designs)


class _CountPossibilities(Protocol):
    def __call__(self, design: str) -> int: ...


def _get_count_possibilities(towels: list[str]) -> _CountPossibilities:
    @functools.cache
    def count_possibilities(design: str) -> int:
        if not design:
            return 1
        count = 0
        for towel in towels:
            if design.startswith(towel):
                count += count_possibilities(design[len(towel) :])
        return count

    return count_possibilities
