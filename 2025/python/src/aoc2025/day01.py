from pathlib import Path


def part_1(input: Path) -> int:
    dial = 50
    password = 0
    for instruction in input.read_text().splitlines():
        delta_dial = int(instruction[1:])
        if instruction.startswith("R"):
            dial = (dial + delta_dial) % 100
        else:
            dial = (dial - delta_dial) % 100
        if dial == 0:
            password += 1
    return password


def part_2(input: Path) -> int:
    dial = 50
    password = 0
    for instruction in input.read_text().splitlines():
        delta_dial = int(instruction[1:])
        if instruction.startswith("R"):
            password += (dial + delta_dial) // 100
            dial = (dial + delta_dial) % 100
        else:
            if delta_dial >= dial:
                if dial == 0:
                    password += delta_dial // 100
                else:
                    password += 1 + (delta_dial - dial) // 100
            dial = (dial - delta_dial) % 100

    return password
