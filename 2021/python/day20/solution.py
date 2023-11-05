import collections
import itertools


def print_image(image: dict[tuple[int, int], bool]) -> None:
    i_min = min([i for (i, _) in image])
    j_min = min([j for (_, j) in image])
    i_max = max([i for (i, _) in image])
    j_max = max([j for (_, j) in image])
    s = ""
    for i in range(i_min, i_max + 1):
        s_line = ""
        for j in range(j_min, j_max + 1):
            if image[(i, j)]:
                s_line += "#"
            else:
                s_line += "."
        s += s_line + "\n"
    print(s)


def solve(file_path: str, n_steps: int) -> int:
    with open(file_path, "r") as f:
        algorithm_raw_data, image_raw_data = f.read().split("\n\n")

    algorithm = tuple([char == "#" for char in list(algorithm_raw_data)])
    flashing = algorithm[0]
    if flashing:
        assert not algorithm[-1]
        assert n_steps % 2 == 0

    image = collections.defaultdict(lambda: False)
    for i, line in enumerate(image_raw_data.splitlines()):
        for j, char in enumerate(list(line)):
            image[(i, j)] = char == "#"
    i_min, j_min = 0, 0
    i_max = max([i for (i, _) in image])
    j_max = max([j for (_, j) in image])

    for step in range(n_steps):
        if flashing:
            default = bool(step % 2)
        else:
            default = False
        next_image = collections.defaultdict(lambda: default)
        for i, j in itertools.product(
            range(i_min - 1, i_max + 2), range(j_min - 1, j_max + 2)
        ):
            algorithm_idx = 0
            for idx, (di, dj) in enumerate(
                reversed(list(itertools.product(range(-1, 2), range(-1, 2))))
            ):
                if image[(i + di, j + dj)]:
                    algorithm_idx += 1 << idx
            next_image[(i, j)] = algorithm[algorithm_idx]
        image = next_image
        i_min -= 1
        j_min -= 1
        i_max += 1
        j_max += 1

    return sum(image.values())
