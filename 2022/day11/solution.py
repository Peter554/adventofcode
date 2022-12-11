from __future__ import annotations

import dataclasses
import re
from collections import deque
from typing import Callable
import functools


@dataclasses.dataclass
class Monkey:
    id: int
    item_worries: deque[int]
    inspection_operation: Callable[[int], int]
    test_division_factor: int
    test_positive_monkey_id: int
    test_negative_monkey_id: int

    def __post_init__(self):
        self.inspection_count = 0

    @classmethod
    def parse(cls, s: str) -> Monkey:
        lines = deque(s.splitlines())

        match = re.match(r"^Monkey (\d+):$", lines.popleft().strip())
        assert match is not None
        id_ = int(match.group(1))

        match = re.match(r"^Starting items: (.+)$", lines.popleft().strip())
        assert match is not None
        item_worries = deque(int(worry) for worry in match.group(1).split(", "))

        match = re.match(
            r"^Operation: new = old (\+|\*) (old|\d+)$", lines.popleft().strip()
        )
        assert match is not None
        if match.group(1) == "+":
            if match.group(2) == "old":
                inspection_operation = lambda x: x + x
            else:
                n = int(match.group(2))
                inspection_operation = lambda x: x + n
        else:
            if match.group(2) == "old":
                inspection_operation = lambda x: x * x
            else:
                n = int(match.group(2))
                inspection_operation = lambda x: x * n

        match = re.match(r"^Test: divisible by (\d+)$", lines.popleft().strip())
        assert match is not None
        test_division_factor = int(match.group(1))
        match = re.match(r"^If true: throw to monkey (\d+)$", lines.popleft().strip())
        assert match is not None
        test_positive_monkey_id = int(match.group(1))
        match = re.match(r"^If false: throw to monkey (\d+)$", lines.popleft().strip())
        assert match is not None
        test_negative_monkey_id = int(match.group(1))

        return cls(
            id_,
            item_worries,
            inspection_operation,
            test_division_factor,
            test_positive_monkey_id,
            test_negative_monkey_id,
        )

    def act(
        self, monkeys: dict[int, Monkey], relief_operation: Callable[[int], int]
    ) -> None:
        while self.item_worries:
            initial_worry = self.item_worries.popleft()
            worry = relief_operation(self.inspection_operation(initial_worry))
            throw_monkey_id = (
                self.test_positive_monkey_id
                if worry % self.test_division_factor == 0
                else self.test_negative_monkey_id
            )
            monkeys[throw_monkey_id].item_worries.append(worry)
            self.inspection_count += 1


def part_1(file_path: str) -> int:
    with open(file_path) as f:
        raw_monkeys = f.read().split("\n\n")
    monkeys_list = [Monkey.parse(raw_monkey) for raw_monkey in raw_monkeys]
    monkeys = {monkey.id: monkey for monkey in monkeys_list}

    for _ in range(20):
        for monkey in monkeys.values():
            monkey.act(monkeys, lambda worry: worry // 3)

    monkey_inspection_counts = sorted(
        [monkey.inspection_count for monkey in monkeys.values()], reverse=True
    )
    return monkey_inspection_counts[0] * monkey_inspection_counts[1]


def part_2(file_path: str) -> int:
    with open(file_path) as f:
        raw_monkeys = f.read().split("\n\n")
    monkeys_list = [Monkey.parse(raw_monkey) for raw_monkey in raw_monkeys]
    monkeys = {monkey.id: monkey for monkey in monkeys_list}

    test_division_factor_product = functools.reduce(
        lambda a, b: a * b,
        [monkey.test_division_factor for monkey in monkeys.values()],
    )

    for _ in range(10_000):
        for monkey in monkeys.values():
            monkey.act(monkeys, lambda worry: worry % test_division_factor_product)

    monkey_inspection_counts = sorted(
        [monkey.inspection_count for monkey in monkeys.values()], reverse=True
    )
    return monkey_inspection_counts[0] * monkey_inspection_counts[1]
