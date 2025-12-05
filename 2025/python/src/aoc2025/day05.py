import dataclasses
from pathlib import Path


@dataclasses.dataclass(frozen=True)
class Range:
    start: int
    end: int

    @property
    def size(self) -> int:
        return self.end - self.start + 1

    def __contains__(self, item: int) -> bool:
        return self.start <= item <= self.end


def part_1(input: Path) -> int:
    ranges, ids = parse_input(input)
    ranges = sort_and_merge(ranges)
    count_fresh = 0
    for id_ in ids:
        for range_ in ranges:
            if id_ in range_:
                count_fresh += 1
                break
    return count_fresh


def part_2(input: Path) -> int:
    ranges, _ = parse_input(input)
    ranges = sort_and_merge(ranges)
    return sum(r.size for r in ranges)


def parse_input(input: Path) -> tuple[list[Range], list[int]]:
    raw_ranges, raw_ids = input.read_text().split("\n\n")
    fresh_ingredient_ranges = [
        Range(int(r.split("-")[0]), int(r.split("-")[1]))
        for r in raw_ranges.splitlines()
    ]
    ingredient_ids = [int(r) for r in raw_ids.splitlines()]
    return fresh_ingredient_ranges, ingredient_ids


def sort_and_merge(ranges: list[Range]) -> list[Range]:
    ranges = sorted(ranges, key=lambda r: r.start)
    merged_ranges = [ranges[0]]
    for range_ in ranges[1:]:
        if range_.start <= merged_ranges[-1].end:
            merged_ranges[-1] = Range(
                merged_ranges[-1].start,
                max(merged_ranges[-1].end, range_.end),
            )
        else:
            merged_ranges.append(range_)
    return merged_ranges
