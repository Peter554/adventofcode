import statistics


def part_1(file_path: str) -> int:
    with open(file_path, "r") as f:
        lines = f.read().splitlines()
    gamma, l = 0, len(lines[0])
    for i in range(l):
        if statistics.mode([line[i] for line in lines]) == "1":
            gamma |= 1 << (l - i - 1)
    epsilon = gamma ^ ((1 << l) - 1)
    return gamma * epsilon


def part_2(file_path: str) -> int:
    with open(file_path, "r") as f:
        lines = f.read().splitlines()
    ox, co2, l = 0, 0, len(lines[0])

    ox_lines = lines
    for i in range(l):
        multimode = statistics.multimode([line[i] for line in ox_lines])
        mode = multimode[0] if len(multimode) == 1 else "1"
        ox_lines = [line for line in ox_lines if line[i] == mode]
        if len(ox_lines) == 1:
            ox = int(ox_lines[0], 2)
            break

    co2_lines = lines
    for i in range(l):
        multimode = statistics.multimode([line[i] for line in co2_lines])
        mode = multimode[0] if len(multimode) == 1 else "1"
        co2_lines = [line for line in co2_lines if line[i] == f"{1-int(mode)}"]
        if len(co2_lines) == 1:
            co2 = int(co2_lines[0], 2)
            break

    return ox * co2
