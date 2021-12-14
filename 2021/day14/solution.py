from __future__ import annotations

import collections
import functools


def simulate_polymer(file_path: str, n_steps: int) -> int:
    with open(file_path, "r") as f:
        template_data, rules_data = f.read().split("\n\n")

    template = tuple(template_data)
    rules = {}
    for rule_data in rules_data.splitlines():
        from_pair, to = rule_data.split(" -> ")
        rules[tuple(from_pair)] = to

    @functools.cache
    def counts_between(
        value_left: str, value_right: str, depth: int
    ) -> collections.Counter[str]:
        if depth == 0:
            return collections.Counter([value_left, value_right])
        else:
            value_middle = rules[(value_left, value_right)]
            return (
                counts_between(value_left, value_middle, depth - 1)
                + counts_between(value_middle, value_right, depth - 1)
                - collections.Counter([value_middle])
            )

    counts = collections.Counter[str]()
    for i in range(len(template) - 1):
        counts += counts_between(template[i], template[i + 1], n_steps)
    for i in range(1, len(template) - 1):
        counts -= collections.Counter([template[i]])
    return max(counts.values()) - min(counts.values())


def part_1(file_path: str) -> int:
    return simulate_polymer(file_path, 10)


def part_2(file_path: str) -> int:
    return simulate_polymer(file_path, 40)
