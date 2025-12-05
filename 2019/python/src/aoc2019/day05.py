import dataclasses
from pathlib import Path


def part1(input: Path) -> int:
    code = [int(n) for n in input.read_text().split(",")]
    return Intcode(code, [1]).run()[-1]


def part2(input: Path) -> int:
    code = [int(n) for n in input.read_text().split(",")]
    return Intcode(code, [5]).run()[-1]


@dataclasses.dataclass
class Intcode:
    _code: list[int]
    _inputs: list[int]
    _ip: int = 0

    def run(self) -> list[int]:
        outputs = []
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
                    self._set(self._ip + 1, parameter_modes[0], self._inputs.pop(0))
                    self._ip += 2
                case 4:
                    outputs.append(self._get(self._ip + 1, parameter_modes[0]))
                    self._ip += 2
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
                    break
                case _:
                    raise ValueError(f"Invalid opcode {opcode}")
        return outputs

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
