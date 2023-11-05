def part_1(file_path: str) -> int:
    with open(file_path, "r") as f:
        dots_data, instructions_data = f.read().split("\n\n")

    dots: set[tuple[int, int]] = set()
    for line in dots_data.splitlines():
        x_str, y_str = line.split(",")
        dots.add((int(x_str), int(y_str)))
    instructions: list[tuple[str, int]] = []
    for line in instructions_data.splitlines():
        line = line.lstrip("fold along ")
        d, n_str = line.split("=")
        instructions.append((d, int(n_str)))

    for d, n in instructions:
        if d == "x":
            for dot in dots.copy():
                if dot[0] > n:
                    dots.remove(dot)
                    dots.add((2 * n - dot[0], dot[1]))
        if d == "y":
            for dot in dots.copy():
                if dot[1] > n:
                    dots.remove(dot)
                    dots.add((dot[0], 2 * n - dot[1]))
        break

    return len(dots)


def part_2(file_path: str) -> str:
    with open(file_path, "r") as f:
        dots_data, instructions_data = f.read().split("\n\n")

    dots: set[tuple[int, int]] = set()
    for line in dots_data.splitlines():
        x_str, y_str = line.split(",")
        dots.add((int(x_str), int(y_str)))
    instructions: list[tuple[str, int]] = []
    for line in instructions_data.splitlines():
        line = line.lstrip("fold along ")
        d, n_str = line.split("=")
        instructions.append((d, int(n_str)))

    for d, n in instructions:
        if d == "x":
            for (x, y) in dots.copy():
                if x > n:
                    dots.remove((x, y))
                    dots.add((2 * n - x, y))
        if d == "y":
            for (x, y) in dots.copy():
                if y > n:
                    dots.remove((x, y))
                    dots.add((x, 2 * n - y))

    x_max, y_max = max([x for (x, _) in dots]), max([y for (_, y) in dots])
    s = ""
    for y in range(y_max + 1):
        for x in range(x_max + 1):
            if (x, y) in dots:
                s += "#"
            else:
                s += "."
        s += "\n"
    return s.strip()
