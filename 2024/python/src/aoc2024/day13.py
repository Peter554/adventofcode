import re
from pathlib import Path

import z3


def part_1(input: Path) -> int:
    return solve(input, 0)


def part_2(input: Path) -> int:
    return solve(input, 10000000000000)


def solve(input: Path, target_offset: int) -> int:
    tokens = 0

    for machine in input.read_text().split("\n\n"):
        lines = machine.splitlines()
        a_x = _match(r"X\+(\d+)", lines[0])
        a_y = _match(r"Y\+(\d+)", lines[0])
        b_x = _match(r"X\+(\d+)", lines[1])
        b_y = _match(r"Y\+(\d+)", lines[1])
        target_x = _match(r"X=(\d+)", lines[2]) + target_offset
        target_y = _match(r"Y=(\d+)", lines[2]) + target_offset

        solver = z3.Solver()
        a_presses = z3.Int("a_presses")
        b_presses = z3.Int("b_presses")
        solver.add(target_x == a_presses * a_x + b_presses * b_x)
        solver.add(target_y == a_presses * a_y + b_presses * b_y)
        if solver.check() == z3.sat:
            tokens += (
                3 * solver.model()[a_presses].as_long()
                + solver.model()[b_presses].as_long()
            )

    return tokens


def _match(pattern: str, s: str) -> int:
    match = re.search(pattern, s)
    assert match is not None
    return int(match.group(1))
