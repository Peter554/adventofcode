def part_1(file_path: str) -> int:
    with open(file_path, "r") as f:
        heights = [[int(n) for n in list(line.strip())] for line in f]
    count = 0
    for i, row in enumerate(heights):
        for j, height in enumerate(heights[i]):
            low = True
            for (i2, j2) in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
                if i2 < 0 or i2 >= len(heights) or j2 < 0 or j2 >= len(heights[0]):
                    continue
                if heights[i2][j2] <= height:
                    low = False
                    break
            if low:
                count += height + 1
    return count


def part_2(file_path: str) -> int:
    with open(file_path, "r") as f:
        heights = [[int(n) for n in list(line.strip())] for line in f]

    points: set[tuple[int, int]] = set()
    for i, row in enumerate(heights):
        for j, height in enumerate(heights[i]):
            if height == 9:
                continue
            points.add((i, j))

    basins: list[int] = []
    while points:
        p = points.pop()
        basin = {p}
        to_check = {p}
        while to_check:
            for (i, j) in [*to_check]:
                for (i2, j2) in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
                    if (i2, j2) in points:
                        basin.add((i2, j2))
                        to_check.add((i2, j2))
                        points.remove((i2, j2))
                to_check.remove((i, j))
        basins.append(len(basin))

    basins.sort(reverse=True)
    return basins[0] * basins[1] * basins[2]
