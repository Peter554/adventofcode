from pathlib import Path


def part_1(input: Path) -> int:
    total_joltage = 0
    for bank in input.read_text().splitlines():
        first_joltage, second_joltage = 0, 0
        for idx, joltage in enumerate(bank):
            joltage = int(joltage)
            if idx <= len(bank) - 2 and joltage > first_joltage:
                first_joltage = joltage
                second_joltage = 0
            elif joltage > second_joltage:
                second_joltage = joltage
        total_joltage += int(f"{first_joltage}{second_joltage}")
    return total_joltage


def part_2(input: Path) -> int:
    total_joltage = 0
    for bank in input.read_text().splitlines():
        joltages = [0] * 12
        for idx, joltage in enumerate(bank):
            joltage = int(joltage)
            for idx2 in range(12):
                if idx <= len(bank) - (12 - idx2) and joltage > joltages[idx2]:
                    joltages[idx2] = joltage
                    joltages[idx2 + 1 :] = [0] * (12 - (idx2 + 1))
                    break
        total_joltage += int("".join(str(j) for j in joltages))
    return total_joltage
