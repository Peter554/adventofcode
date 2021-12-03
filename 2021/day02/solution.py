def part_1(file_path: str) -> int:
    with open(file_path, "r") as f:
        lines = f.read().splitlines()
    x, depth = 0, 0
    for line in lines:
        cmd, n = line.split()
        if cmd == "forward":
            x += int(n)
        elif cmd == "down":
            depth += int(n)
        elif cmd == "up":
            depth -= int(n)
    return x * depth


def part_2(file_path: str) -> int:
    with open(file_path, "r") as f:
        lines = f.read().splitlines()
    x, depth, aim = 0, 0, 0
    for line in lines:
        cmd, n = line.split()
        if cmd == "forward":
            x += int(n)
            depth += aim * int(n)
        elif cmd == "down":
            aim += int(n)
        elif cmd == "up":
            aim -= int(n)
    return x * depth
