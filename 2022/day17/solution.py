import itertools

from common.point2d import Point2D

rock_templates = [
    # ####
    [(1, 1), (2, 1), (3, 1), (4, 1)],
    # .#.
    # ###
    # .#.
    [(2, 1), (1, 2), (2, 2), (3, 2), (2, 3)],
    # ..#
    # ..#
    # ###
    [(1, 1), (2, 1), (3, 1), (3, 2), (3, 3)],
    # #
    # #
    # #
    # #
    [(1, 1), (1, 2), (1, 3), (1, 4)],
    # ##
    # ##
    [(1, 1), (2, 1), (1, 2), (2, 2)],
]


def move_rock(rock: frozenset[Point2D], delta: Point2D) -> frozenset[Point2D]:
    return frozenset(p + delta for p in rock)


def print_rubble(rubble: set[Point2D], max_y: int):
    s = ""
    for y in range(max_y, 0, -1):
        for x in range(1, 8):
            if Point2D(x, y) in rubble:
                s += "#"
            else:
                s += "."
        s += "\n"
    print(s)


def part_1(file_path: str) -> int:
    with open(file_path) as f:
        air_cycle = itertools.cycle(
            {
                "<": Point2D(-1, 0),
                ">": Point2D(1, 0),
            }[char]
            for char in f.readline().strip()
        )

    rock_cycle = itertools.cycle(
        frozenset(Point2D(x, y) for x, y in rock_template)
        for rock_template in rock_templates
    )

    rubble: set[Point2D] = set()
    rubble_height = 0

    def try_move_rock(
        rock: frozenset[Point2D], delta: Point2D
    ) -> tuple[bool, frozenset[Point2D]]:
        moved_rock = move_rock(rock, delta)
        if any(p.x < 1 for p in moved_rock):
            return False, rock
        if any(p.x > 7 for p in moved_rock):
            return False, rock
        if any(p.y < 1 for p in moved_rock):
            return False, rock
        if len(moved_rock.intersection(rubble)):
            return False, rock
        return True, moved_rock

    for _ in range(2022):
        rock = next(rock_cycle)
        rock = move_rock(rock, Point2D(2, 3 + rubble_height))
        while True:
            _, rock = try_move_rock(rock, next(air_cycle))
            moved, rock = try_move_rock(rock, Point2D(0, -1))
            if not moved:
                rubble = rubble.union(rock)
                rubble_height = max(p.y for p in rubble)
                # print_rubble(rubble, rubble_height)
                break

    return rubble_height
