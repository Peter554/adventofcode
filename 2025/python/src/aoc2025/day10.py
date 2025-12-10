from __future__ import annotations

import dataclasses
import itertools
from pathlib import Path

import z3


def part_1(input: Path) -> int:
    @dataclasses.dataclass(frozen=True)
    class Machine:
        target: int
        buttons: tuple[int, ...]

    def parse_machine(s: str) -> Machine:
        target = int(
            s.split("]")[0][1:][::-1].replace(".", "0").replace("#", "1"), base=2
        )
        buttons = []
        for raw_button in s.split("]")[1].split("{")[0].strip().split():
            button = 0
            for i in map(int, raw_button[1:-1].split(",")):
                button += 1 << i
            buttons.append(button)
        return Machine(target, tuple(buttons))

    machines = [parse_machine(line) for line in input.read_text().splitlines()]

    def get_button_presses(machine: Machine) -> int:
        for n_presses in range(len(machine.buttons) + 1):
            for buttons in itertools.combinations(machine.buttons, n_presses):
                state = 0
                for button in buttons:
                    state ^= button
                if state == machine.target:
                    return n_presses
        return -1

    return sum(get_button_presses(machine) for machine in machines)


def part_2(input: Path) -> int:
    @dataclasses.dataclass(frozen=True)
    class Machine:
        buttons: tuple[frozenset[int], ...]
        targets: tuple[int, ...]

    def parse_machine(s: str) -> Machine:
        buttons = []
        for raw_button in s.split("]")[1].split("{")[0].strip().split():
            buttons.append(frozenset(eval(raw_button[:-1] + ",)")))
        targets = eval("(" + s.split("{")[1][:-1] + ")")
        return Machine(tuple(buttons), targets)

    machines = [parse_machine(line) for line in input.read_text().splitlines()]

    def get_button_presses(machine: Machine) -> int:
        solver = z3.Optimize()
        all_button_presses = [
            z3.Int(f"button_presses_{idx}") for idx, _ in enumerate(machine.buttons)
        ]
        # Constraint: Buttons must be pushed >= 0 times.
        solver.add([button_presses >= 0 for button_presses in all_button_presses])
        # Constraint: Sum of button pushes affecting a joltage must equal the target joltage.
        for target_idx, target in enumerate(machine.targets):
            button_presses_affecting_target = (
                button_presses
                for button_presses, button in zip(all_button_presses, machine.buttons)
                if target_idx in button
            )
            solver.add(target == z3.Sum(button_presses_affecting_target))
        # Objective: Minimize total number of button pushes.
        solver.minimize(z3.Sum(all_button_presses))

        assert solver.check() == z3.sat
        return sum(
            solver.model()[button_presses].as_long()
            for button_presses in all_button_presses
        )

    return sum(get_button_presses(machine) for machine in machines)
