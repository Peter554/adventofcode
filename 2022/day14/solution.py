import enum


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
