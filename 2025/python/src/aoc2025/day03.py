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
        bank_joltages: str = ""
        window_start_idx, window_end_idx = 0, -11
        for _ in range(12):
            window = bank[window_start_idx : (window_end_idx or None)]
            window_max_joltage = max(window)
            bank_joltages += window_max_joltage
            window_start_idx += window.index(window_max_joltage) + 1
            window_end_idx += 1
        total_joltage += int(bank_joltages)
    return total_joltage
