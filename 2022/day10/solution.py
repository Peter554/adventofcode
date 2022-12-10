def part_1(file_path: str) -> int:
    with open(file_path) as f:
        instructions = [line.strip() for line in f.readlines()]

    cycle, x = 0, 1
    signal_strengths = []

    def on_cycle_start():
        if cycle in [20, 60, 100, 140, 180, 220]:
            signal_strengths.append(cycle * x)

    for instruction in instructions:
        if instruction == "noop":
            cycle += 1
            on_cycle_start()
        else:
            # addx
            _, dx = instruction.split(" ")
            cycle += 1
            on_cycle_start()
            #
            cycle += 1
            on_cycle_start()
            x += int(dx)

    return sum(signal_strengths)


def part_2(file_path: str) -> str:
    with open(file_path) as f:
        instructions = [line.strip() for line in f.readlines()]

    cycle, x = 0, 1
    pixels: list[list[str]] = [[]]

    def add_pixel():
        if len(pixels[-1]) == 40:
            pixels.append([])
        if (cycle - 1) % 40 in [x - 1, x, x + 1]:
            pixels[-1].append("#")
        else:
            pixels[-1].append(".")

    for instruction in instructions:
        if instruction == "noop":
            cycle += 1
            add_pixel()
        else:
            # addx
            _, dx = instruction.split(" ")
            cycle += 1
            add_pixel()
            #
            cycle += 1
            add_pixel()
            x += int(dx)

    return "\n".join("".join(pixels_line) for pixels_line in pixels)
