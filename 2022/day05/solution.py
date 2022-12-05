import re
from typing import Protocol


class InstructionHandler(Protocol):
    def handle(
        self, *, n_move: int, from_stack: list[str], to_stack: list[str]
    ) -> None:
        ...


def solve(file_path: str, instruction_handler: InstructionHandler) -> str:
    with open(file_path) as f:
        init, instructions = [s.splitlines() for s in f.read().split("\n\n")]

    stacks: list[list[str]] = []
    for init_match in re.finditer(r"\d", init[-1]):
        stacks.append([])
        for init_line in init[-2::-1]:
            value = init_line[init_match.start()]
            if value == " ":
                break
            stacks[-1].append(value)

    for instruction in instructions:
        instruction_match = re.match(r"^move (\d+) from (\d+) to (\d+)$", instruction)
        assert instruction_match is not None
        n_move = int(instruction_match.group(1))
        from_stack = stacks[int(instruction_match.group(2)) - 1]
        to_stack = stacks[int(instruction_match.group(3)) - 1]
        instruction_handler.handle(
            n_move=n_move, from_stack=from_stack, to_stack=to_stack
        )

    return "".join(stack.pop() for stack in stacks)


class Part1InstructionHandler:
    @staticmethod
    def handle(*, n_move: int, from_stack: list[str], to_stack: list[str]) -> None:
        to_stack.extend([from_stack.pop() for _ in range(n_move)])


def part_1(file_path: str) -> str:
    return solve(file_path, Part1InstructionHandler)


class Part2InstructionHandler:
    @staticmethod
    def handle(*, n_move: int, from_stack: list[str], to_stack: list[str]) -> None:
        to_stack.extend(reversed([from_stack.pop() for _ in range(n_move)]))


def part_2(file_path: str) -> str:
    return solve(file_path, Part2InstructionHandler)
