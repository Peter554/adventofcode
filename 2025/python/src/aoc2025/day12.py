import dataclasses
from pathlib import Path


def part_1(input: Path) -> int:
    present_sizes = tuple(s.count("#") for s in input.read_text().split("\n\n")[:-1])
    boxes = tuple(
        parse_box(s) for s in input.read_text().split("\n\n")[-1].splitlines()
    )

    # The puzzle input is specially designed such that this simple check works.
    # The puzzle input in this case is much easier than the example!
    fit = 0
    for box in boxes:
        available_space = box.dimensions[0] * box.dimensions[1]
        for present_size, present_count in zip(present_sizes, box.present_counts):
            available_space -= present_size * present_count
            if available_space < 0:
                break
        else:
            fit += 1
    return fit


@dataclasses.dataclass(frozen=True)
class Box:
    dimensions: tuple[int, int]
    present_counts: tuple[int, ...]


def parse_box(s: str) -> Box:
    width, height = map(int, s.split(":")[0].split("x"))
    present_counts = map(int, s.split(":")[1].strip().split())
    return Box((width, height), tuple(present_counts))
