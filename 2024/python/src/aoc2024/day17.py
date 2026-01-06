from pathlib import Path


def part_1(input: Path) -> str:
    lines = input.read_text().splitlines()
    a = int(lines[0].split(":")[1].strip())
    b = int(lines[1].split(":")[1].strip())
    c = int(lines[2].split(":")[1].strip())
    program = list(map(int, lines[4].split(":")[1].strip().split(",")))
    return run_program(program, a, b, c)


def part_2() -> int:
    """
    Program: 2,4,1,4,7,5,4,1,1,4,5,5,0,3,3,0

    This is equivalent to:

    ```
    do:
        b = a % 8
        b = b ^ 4   # b = (a % 8) ^ 4
        c = a >> b  # c = a >> ((a % 8) ^ 4)
        b = b ^ c   # b = (a % 8) ^ 4 ^ c
        b = b ^ 4   # b = (a % 8) ^ 4 ^ c ^ 4 = (a % 8) ^ c
        out: b % 8  # out: ((a % 8) ^ (a >> ((a % 8) ^ 4))) % 8
        a = a >> 3  # Lose 3 bits of a
    while:
        a != 0
    ```

    - Lose 3 bits of a every iteration
    - One output per iteration
    - We know that a is 0 at the end
    """

    def get_output(a: int) -> int:
        return ((a % 8) ^ (a >> ((a % 8) ^ 4))) % 8

    solutions = set()

    def solve(program: list[int], a: int):
        if not program:
            solutions.add(a)
            return

        for candidate_next_bits in range(8):
            candidate_a = (a << 3) | candidate_next_bits
            if candidate_a != 0 and get_output(candidate_a) == program[-1]:
                solve(program[:-1], candidate_a)

    solve([2, 4, 1, 4, 7, 5, 4, 1, 1, 4, 5, 5, 0, 3, 3, 0], 0)

    return min(solutions)


def run_program(program: list[int], a: int, b: int, c: int) -> str:
    def literal(operand: int) -> int:
        return operand

    def combo(operand: int) -> int:
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return a
            case 5:
                return b
            case 6:
                return c
            case _:
                raise ValueError(f"Invalid combo operand: {operand}")

    ip = 0
    output: list[int] = []
    while ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1]
        match opcode:
            case 0:
                numerator = a
                denominator = 2 ** combo(operand)
                a = numerator // denominator
                ip += 2
            case 1:
                b = b ^ literal(operand)
                ip += 2
            case 2:
                b = combo(operand) % 8
                ip += 2
            case 3:
                if a == 0:
                    ip += 2
                else:
                    ip = literal(operand)
            case 4:
                b = b ^ c
                # operand unused.
                ip += 2
            case 5:
                output.append(combo(operand) % 8)
                ip += 2
            case 6:
                numerator = a
                denominator = 2 ** combo(operand)
                b = numerator // denominator
                ip += 2
            case 7:
                numerator = a
                denominator = 2 ** combo(operand)
                c = numerator // denominator
                ip += 2
    return ",".join(map(str, output))
