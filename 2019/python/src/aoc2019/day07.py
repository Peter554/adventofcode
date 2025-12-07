import dataclasses
import itertools
from pathlib import Path
from typing import Self


def part1(input: Path) -> int:
    code = [int(n) for n in input.read_text().split(",")]
    largest_signal = 0
    for phases in itertools.permutations(range(5)):
        amps = [IntcodeVM(code.copy(), [phase]) for phase in phases]
        amps[0].push_input(0)
        amps[1].push_input(amps[0].run_until_halted().outputs[-1])
        amps[2].push_input(amps[1].run_until_halted().outputs[-1])
        amps[3].push_input(amps[2].run_until_halted().outputs[-1])
        amps[4].push_input(amps[3].run_until_halted().outputs[-1])
        if (signal := amps[4].run_until_halted().outputs[-1]) > largest_signal:
            largest_signal = signal
    return largest_signal


def part2(input: Path) -> int:
    code = [int(n) for n in input.read_text().split(",")]
    largest_signal = 0
    for phases in itertools.permutations(range(5, 10)):
        # Set up amps
        amps = [IntcodeVM(code.copy(), [phase]) for phase in phases]
        amps[0].push_input(0)
        # Run the amps
        while True:
            all_halted = True
            for idx, amp in enumerate(amps):
                output = amp.run_until_next_output()
                match output:
                    case InputRequired():
                        all_halted = False
                    case ProgramHalted():
                        ...
                    case int():
                        all_halted = False
                        amps[(idx + 1) % len(amps)].push_input(output)
            if all_halted:
                break
        if (signal := amps[-1].outputs[-1]) > largest_signal:
            largest_signal = signal
    return largest_signal


@dataclasses.dataclass(frozen=True)
class InputRequired: ...


@dataclasses.dataclass(frozen=True)
class ProgramHalted: ...


class InputRequiredError(Exception): ...


class IntcodeVM:
    def __init__(self, code: list[int], inputs: list[int]) -> None:
        self._code = code.copy()
        self._inputs = inputs.copy()
        self._outputs: list[int] = []
        self._ip: int = 0

    def push_input(self, value: int) -> None:
        self._inputs.append(value)

    @property
    def outputs(self) -> tuple[int, ...]:
        return tuple(self._outputs)

    def run_until_next_output(self) -> int | InputRequired | ProgramHalted:
        while True:
            opcode, parameter_modes = self._parse_opcode(self._code[self._ip])
            match opcode:
                case 1:
                    self._set(
                        self._ip + 3,
                        parameter_modes[2],
                        self._get(self._ip + 1, parameter_modes[0])
                        + self._get(self._ip + 2, parameter_modes[1]),
                    )
                    self._ip += 4
                case 2:
                    self._set(
                        self._ip + 3,
                        parameter_modes[2],
                        self._get(self._ip + 1, parameter_modes[0])
                        * self._get(self._ip + 2, parameter_modes[1]),
                    )
                    self._ip += 4
                case 3:
                    if not self._inputs:
                        return InputRequired()
                    self._set(self._ip + 1, parameter_modes[0], self._inputs.pop(0))
                    self._ip += 2
                case 4:
                    output = self._get(self._ip + 1, parameter_modes[0])
                    self._outputs.append(output)
                    self._ip += 2
                    return output
                case 5:
                    jump = self._get(self._ip + 1, parameter_modes[0]) != 0
                    if jump:
                        self._ip = self._get(self._ip + 2, parameter_modes[1])
                    else:
                        self._ip += 3
                case 6:
                    jump = self._get(self._ip + 1, parameter_modes[0]) == 0
                    if jump:
                        self._ip = self._get(self._ip + 2, parameter_modes[1])
                    else:
                        self._ip += 3
                case 7:
                    self._set(
                        self._ip + 3,
                        parameter_modes[2],
                        int(
                            self._get(self._ip + 1, parameter_modes[0])
                            < self._get(self._ip + 2, parameter_modes[1])
                        ),
                    )
                    self._ip += 4
                case 8:
                    self._set(
                        self._ip + 3,
                        parameter_modes[2],
                        int(
                            self._get(self._ip + 1, parameter_modes[0])
                            == self._get(self._ip + 2, parameter_modes[1])
                        ),
                    )
                    self._ip += 4
                case 99:
                    return ProgramHalted()
                case _:
                    raise ValueError(f"Invalid opcode {opcode}")

    def run_until_halted(self) -> Self:
        while True:
            output = self.run_until_next_output()
            match output:
                case InputRequired():
                    raise InputRequiredError
                case ProgramHalted():
                    return self
                case int():
                    ...

    @staticmethod
    def _parse_opcode(opcode: int) -> tuple[int, tuple[int, ...]]:
        s = str(opcode).zfill(5)
        return int(s[3:]), (int(s[2]), int(s[1]), int(s[0]))

    def _get(self, parameter_ip: int, parameter_mode: int) -> int:
        match parameter_mode:
            case 0:
                return self._code[self._code[parameter_ip]]
            case 1:
                return self._code[parameter_ip]
            case _:
                raise ValueError(f"Invalid parameter mode {parameter_mode}")

    def _set(self, parameter_ip: int, parameter_mode: int, value: int) -> None:
        match parameter_mode:
            case 0:
                self._code[self._code[parameter_ip]] = value
            case 1:
                self._code[parameter_ip] = value
            case _:
                raise ValueError(f"Invalid parameter mode {parameter_mode}")
