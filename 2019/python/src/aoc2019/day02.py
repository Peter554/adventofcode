from pathlib import Path


def part1(input: Path) -> int:
    code = [int(n) for n in input.read_text().split(",")]
    return run_intcode(code, 12, 2)


def part2(input: Path) -> int:
    code = [int(n) for n in input.read_text().split(",")]
    for noun in range(100):
        for verb in range(100):
            if run_intcode(code.copy(), noun, verb) == 19690720:
                return 100 * noun + verb
    return -1


def run_intcode(code: list[int], noun: int, verb: int) -> int:
    code[1] = noun
    code[2] = verb
    ip = 0
    while True:
        match code[ip]:
            case 1:
                code[code[ip + 3]] = code[code[ip + 1]] + code[code[ip + 2]]
                ip += 4
            case 2:
                code[code[ip + 3]] = code[code[ip + 1]] * code[code[ip + 2]]
                ip += 4
            case 99:
                break
    return code[0]
