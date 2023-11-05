import re


def run_alu_program(program: str, inputs: tuple[int, ...]) -> tuple[int, int, int, int]:
    state = {"w": 0, "x": 0, "y": 0, "z": 0}
    for line in program.strip().splitlines():
        if match := re.match(r"^inp ([wxyz])", line):
            state[match.group(1)] = inputs[0]
            inputs = (*inputs[1:],)
        elif match := re.match(r"^add ([wxyz]) ([wxyz])", line):
            state[match.group(1)] += state[match.group(2)]
        elif match := re.match(r"^add ([wxyz]) (-?\d+)", line):
            state[match.group(1)] += int(match.group(2))
        elif match := re.match(r"^mul ([wxyz]) ([wxyz])", line):
            state[match.group(1)] *= state[match.group(2)]
        elif match := re.match(r"^mul ([wxyz]) (-?\d+)", line):
            state[match.group(1)] *= int(match.group(2))
        elif match := re.match(r"^div ([wxyz]) ([wxyz])", line):
            state[match.group(1)] = int(state[match.group(1)] / state[match.group(2)])
        elif match := re.match(r"^div ([wxyz]) (-?\d+)", line):
            state[match.group(1)] = int(state[match.group(1)] / int(match.group(2)))
        elif match := re.match(r"^mod ([wxyz]) ([wxyz])", line):
            state[match.group(1)] %= state[match.group(2)]
        elif match := re.match(r"^mod ([wxyz]) (-?\d+)", line):
            state[match.group(1)] %= int(match.group(2))
        elif match := re.match(r"^eql ([wxyz]) ([wxyz])", line):
            state[match.group(1)] = (
                1 if state[match.group(1)] == state[match.group(2)] else 0
            )
        elif match := re.match(r"^eql ([wxyz]) (-?\d+)", line):
            state[match.group(1)] = (
                1 if state[match.group(1)] == int(match.group(2)) else 0
            )
    return state["w"], state["x"], state["y"], state["z"]


def monad_is_valid(monad: int) -> bool:
    if monad < 0:
        return False
    inputs = list(map(int, str(monad)))
    if len(inputs) != 14:
        return False
    if 0 in inputs:
        return False
    with open("day24/monad_program") as f:
        program = f.read()
    w, x, y, z = run_alu_program(program, tuple(inputs))
    return z == 0


def monad_is_valid_reduced(monad: int) -> bool:
    if monad < 0:
        return False
    inputs = list(map(int, str(monad)))
    if len(inputs) != 14:
        return False
    if 0 in inputs:
        return False
    inputs.reverse()
    z = 0
    for a, b, c in (
        (1, 15, 13),
        (1, 10, 16),
        (1, 12, 2),
        (1, 10, 8),
        (1, 14, 11),
        (26, -11, 6),
        (1, 10, 12),
        (26, -16, 2),
        (26, -9, 2),
        (1, 11, 15),
        (26, -8, 1),
        (26, -8, 10),
        (26, -10, 14),
        (26, -9, 10),
    ):
        w = inputs.pop()
        x = int((z % 26) + b != w)
        y = (w + c) * x
        z = int(z / a) * (25 * x + 1) + y
    return z == 0
