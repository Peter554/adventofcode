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


def rubble_signature(rubble: set[Point2D], rubble_height: int) -> str:
    s = ""
    for y in range(rubble_height, max(rubble_height - 50, 0), -1):
        for x in range(1, 8):
            s += "1" if Point2D(x, y) in rubble else "0"
    return s


def solve(file_path: str, rocks_to_drop: int) -> int:
    with open(file_path) as f:
        air_cycle = [
            {
                "<": Point2D(-1, 0),
                ">": Point2D(1, 0),
            }[char]
            for char in f.readline().strip()
        ]

    rock_cycle = [
        frozenset(Point2D(x, y) for x, y in rock_template)
        for rock_template in rock_templates
    ]

    rock_idx, air_idx = 0, 0
    remaining_rocks_to_drop = rocks_to_drop
    rubble: set[Point2D] = set()
    rubble_height = 0

    # cycle
    history: dict = {}
    extra_rubble_height = 0

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

    while remaining_rocks_to_drop:
        rocks_dropped = rocks_to_drop - remaining_rocks_to_drop
        history_key = (rubble_signature(rubble, rubble_height), rock_idx, air_idx)
        if history_key in history:
            previous_rocks_dropped, previous_rubble_height = history[history_key]
            delta_rocks_dropped = rocks_dropped - previous_rocks_dropped
            delta_height = rubble_height - previous_rubble_height
            n = remaining_rocks_to_drop // delta_rocks_dropped
            extra_rubble_height += delta_height * n
            remaining_rocks_to_drop -= delta_rocks_dropped * n
        else:
            history[history_key] = (rocks_dropped, rubble_height)

        rock = move_rock(rock_cycle[rock_idx], Point2D(2, 3 + rubble_height))
        rock_idx = (rock_idx + 1) % len(rock_cycle)
        while True:
            _, rock = try_move_rock(rock, air_cycle[air_idx])
            air_idx = (air_idx + 1) % len(air_cycle)
            moved, rock = try_move_rock(rock, Point2D(0, -1))
            if not moved:
                rubble = rubble.union(rock)
                rubble_height = max(p.y for p in rubble)
                remaining_rocks_to_drop -= 1
                break

    return rubble_height + extra_rubble_height


def part_1(file_path: str) -> int:
    return solve(file_path, 2022)


def part_2(file_path: str) -> int:
    return solve(file_path, 1_000_000_000_000)
