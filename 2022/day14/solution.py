import enum

import numpy
from PIL import Image


class CaveTexture(enum.Enum):
    EMPTY = enum.auto()
    ROCK = enum.auto()
    SAND = enum.auto()


Cave = list[list[CaveTexture]]


def initialize_cave(raw_rocks: list[str], floor_depth: int | None) -> Cave:
    from common.point2d import Point2D

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

    cave: list[list[CaveTexture]] = []
    for y in range(max(rock.y for rock in rocks) + 1 + (floor_depth or 1) - 1):
        cave.append([])
        for x in range(1000):  # assume big enough
            cave[-1].append(
                CaveTexture.ROCK if Point2D(x, y) in rocks else CaveTexture.EMPTY
            )
    if floor_depth is not None:
        cave.append([CaveTexture.ROCK] * 1000)
    return cave


def drop_sand(cave: Cave, from_: tuple[int, int] = (500, 0)) -> bool:
    x, y = from_
    if y == len(cave) - 1:
        # falls into the abyss
        return False
    if cave[y + 1][x] not in (CaveTexture.ROCK, CaveTexture.SAND):
        return drop_sand(cave, (x, y + 1))
    elif cave[y + 1][x - 1] not in (CaveTexture.ROCK, CaveTexture.SAND):
        return drop_sand(cave, (x - 1, y + 1))
    elif cave[y + 1][x + 1] not in (CaveTexture.ROCK, CaveTexture.SAND):
        return drop_sand(cave, (x + 1, y + 1))
    cave[y][x] = CaveTexture.SAND
    return True


def count_sand(cave: Cave) -> int:
    return sum(
        cave_texture == CaveTexture.SAND
        for cave_row in cave
        for cave_texture in cave_row
    )


def part_1(file_path: str) -> int:
    with open(file_path) as f:
        raw_rocks = [line.strip() for line in f.readlines()]
    cave = initialize_cave(raw_rocks, None)
    while drop_sand(cave):
        ...
    return count_sand(cave)


def part_2(file_path: str) -> int:
    with open(file_path) as f:
        raw_rocks = [line.strip() for line in f.readlines()]
    cave = initialize_cave(raw_rocks, 2)
    while drop_sand(cave) and cave[0][500] == CaveTexture.EMPTY:
        ...
    return count_sand(cave)


RGB = tuple[int, int, int]


def create_cave_image(
    cave: Cave,
    color_map: dict[CaveTexture, RGB] | None = None,
    size_factor: int = 8,
):
    color_map = color_map or {
        CaveTexture.EMPTY: (211, 211, 211),
        CaveTexture.ROCK: (128, 128, 128),
        CaveTexture.SAND: (194, 178, 128),
    }

    x_min = min(
        x
        for cave_row in cave
        for x, cave_texture in enumerate(cave_row)
        if cave_texture == CaveTexture.SAND
    )
    x_max = max(
        x
        for cave_row in cave
        for x, cave_texture in enumerate(cave_row)
        if cave_texture == CaveTexture.SAND
    )
    img_array = numpy.zeros(
        dtype=numpy.uint8,
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
    while drop_sand(cave) and cave[0][500] == CaveTexture.EMPTY:
        ...
    img = create_cave_image(cave)
    img.save("day14/cave.png")
