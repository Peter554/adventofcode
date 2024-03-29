import enum

import numpy as np
import numpy.typing as npt
from PIL import Image

from common.point2d import Point2D


class CaveTexture(enum.Enum):
    EMPTY = enum.auto()
    ROCK = enum.auto()
    SAND = enum.auto()


Cave = npt.NDArray[np.uint8]


def initialize_cave(raw_rocks: list[str], floor_depth: int | None) -> Cave:
    def normalize(p: Point2D) -> Point2D:
        assert p.x == 0 or p.y == 0
        size = abs(p.x) + abs(p.y)
        return Point2D(p.x // size, p.y // size)

    rocks: set[Point2D] = set()
    for raw_rock in raw_rocks:
        vertices = [
            Point2D(int(raw_vertex.split(",")[0]), int(raw_vertex.split(",")[1]))
            for raw_vertex in raw_rock.split(" -> ")
        ]
        for vertex_from, vertex_to in zip(vertices[:-1], vertices[1:]):
            delta = normalize(vertex_to - vertex_from)
            segment_rocks = [vertex_from]
            while vertex_to != segment_rocks[-1]:
                segment_rocks.append(segment_rocks[-1] + delta)
            rocks.update(segment_rocks)

    cave_height = max(rock.y for rock in rocks) + 1 + (floor_depth or 0)
    cave: Cave = np.zeros(dtype=np.uint8, shape=(cave_height, 1000))
    cave.fill(CaveTexture.EMPTY.value)
    for (y, x), _ in np.ndenumerate(cave):
        if Point2D(x, y) in rocks:
            cave[y, x] = CaveTexture.ROCK.value
    if floor_depth is not None:
        cave[-1, :] = CaveTexture.ROCK.value
    return cave


Path = list[tuple[int, int]]


def drop_sand(cave: Cave, from_: tuple[int, int]) -> tuple[bool, Path]:
    x, y = from_
    if y == len(cave) - 1:
        # falls into the abyss
        return False, [from_]
    if cave[y + 1, x] not in (CaveTexture.ROCK.value, CaveTexture.SAND.value):
        resting, path = drop_sand(cave, (x, y + 1))
        return resting, [from_, *path]
    elif cave[y + 1, x - 1] not in (CaveTexture.ROCK.value, CaveTexture.SAND.value):
        resting, path = drop_sand(cave, (x - 1, y + 1))
        return resting, [from_, *path]
    elif cave[y + 1, x + 1] not in (CaveTexture.ROCK.value, CaveTexture.SAND.value):
        resting, path = drop_sand(cave, (x + 1, y + 1))
        return resting, [from_, *path]
    cave[y, x] = CaveTexture.SAND.value
    return True, [from_]


def count_sand(cave: Cave) -> int:
    return np.count_nonzero(cave == CaveTexture.SAND.value)


def part_1(file_path: str) -> int:
    with open(file_path) as f:
        raw_rocks = [line.strip() for line in f.readlines()]
    cave = initialize_cave(raw_rocks, None)
    path: Path = [(500, 0)]
    while path:
        resting, path_extension = drop_sand(cave, from_=path.pop())
        path.extend(path_extension[:-1])
        if not resting:
            break
    return count_sand(cave)


def part_2(file_path: str) -> int:
    with open(file_path) as f:
        raw_rocks = [line.strip() for line in f.readlines()]
    cave = initialize_cave(raw_rocks, 2)
    path: Path = [(500, 0)]
    while path:
        resting, path_extension = drop_sand(cave, from_=path.pop())
        path.extend(path_extension[:-1])
        if not resting:
            break
    return count_sand(cave)


RGB = tuple[int, int, int]


def create_cave_image(
    cave: Cave,
    color_map: dict[int, RGB] | None = None,
    size_factor: int = 8,
):
    color_map = color_map or {
        CaveTexture.EMPTY.value: (211, 211, 211),
        CaveTexture.ROCK.value: (128, 128, 128),
        CaveTexture.SAND.value: (194, 178, 128),
    }

    x_min = min(
        x
        for cave_row in cave
        for x, cave_texture in enumerate(cave_row)
        if cave_texture == CaveTexture.SAND.value
    )
    x_max = max(
        x
        for cave_row in cave
        for x, cave_texture in enumerate(cave_row)
        if cave_texture == CaveTexture.SAND.value
    )
    img_array = np.zeros(
        dtype=np.uint8,
        shape=(size_factor * len(cave), size_factor * (x_max - x_min + 1), 3),
    )
    for y, cave_row in enumerate(cave):
        for x, cave_texture in enumerate(cave_row[x_min : x_max + 1]):
            img_array[
                y * size_factor : (y + 1) * size_factor,
                x * size_factor : (x + 1) * size_factor,
            ] = color_map[cave_texture]
    return Image.fromarray(img_array, "RGB")


if __name__ == "__main__":
    with open("day14/input") as f:
        raw_rocks = [line.strip() for line in f.readlines()]
    cave = initialize_cave(raw_rocks, 2)
    path: Path = [(500, 0)]
    while path:
        resting, path_extension = drop_sand(cave, from_=path.pop())
        path.extend(path_extension[:-1])
        if not resting:
            break
    img = create_cave_image(cave)
    img.save("day14/cave.png")
