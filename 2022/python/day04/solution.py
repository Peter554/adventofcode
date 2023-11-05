from __future__ import annotations

import dataclasses
import re


@dataclasses.dataclass(frozen=True)
class CleaningRange:
    min_section_id: int
    max_section_id: int

    def overlaps(self, other: CleaningRange) -> bool:
        return (
            self.max_section_id >= other.min_section_id
            and self.min_section_id <= other.max_section_id
        )

    def contains(self, other: CleaningRange) -> bool:
        return (
            self.min_section_id <= other.min_section_id
            and self.max_section_id >= other.max_section_id
        )


@dataclasses.dataclass(frozen=True)
class AssignmentPair:
    range_1: CleaningRange
    range_2: CleaningRange

    @classmethod
    def parse(cls, line: str) -> AssignmentPair:
        match = re.match(r"^(\d+)-(\d+),(\d+)-(\d+)$", line)
        assert match is not None
        return cls(
            CleaningRange(int(match.group(1)), int(match.group(2))),
            CleaningRange(int(match.group(3)), int(match.group(4))),
        )


def part_1(file_path: str) -> int:
    with open(file_path) as f:
        assignment_pairs = [AssignmentPair.parse(line) for line in f]
    return sum(
        assignment_pair.range_1.contains(assignment_pair.range_2)
        or assignment_pair.range_2.contains(assignment_pair.range_1)
        for assignment_pair in assignment_pairs
    )


def part_2(file_path: str) -> int:
    with open(file_path) as f:
        assignment_pairs = [AssignmentPair.parse(line) for line in f]
    return sum(
        assignment_pair.range_1.overlaps(assignment_pair.range_2)
        for assignment_pair in assignment_pairs
    )
