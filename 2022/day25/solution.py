from __future__ import annotations

import dataclasses
import math


def base_5(number: int) -> str:
    if number == 0:
        return "0"
    upper = math.floor(math.log(number, 5))
    s = ""
    for i in range(upper, -1, -1):
        s += str(number // (5**i))
        number %= 5**i
    return s or "0"


OFFSET = sum(2 * (5**i) for i in range(25))


@dataclasses.dataclass(frozen=True)
class SNAFU:
    value: str

    @property
    def decimal(self) -> int:
        d = 0
        for idx, char in enumerate(reversed(self.value)):
            d += (5**idx) * {
                "=": -2,
                "-": -1,
                "0": 0,
                "1": 1,
                "2": 2,
            }[char]
        return d

    @classmethod
    def from_decimal(cls, decimal_value: int) -> SNAFU:
        n = base_5(decimal_value + OFFSET)
        n = n.lstrip("2") or "2"
        return cls(
            n.replace("0", "=")
            .replace("1", "-")
            .replace("2", "0")
            .replace("3", "1")
            .replace("4", "2")
        )

    def __add__(self, other: SNAFU) -> SNAFU:
        return SNAFU.from_decimal(self.decimal + other.decimal)


def part_1(file_path: str) -> str:
    with open(file_path) as f:
        snafus = [SNAFU(line.strip()) for line in f.readlines()]
    total = SNAFU("0")
    for snafu in snafus:
        total += snafu
    return total.value
