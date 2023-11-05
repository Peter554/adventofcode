from day22.base import Point2D, Direction

X_OFFSETS = {
    0: 8,
    1: 0,
    2: 4,
    3: 8,
    4: 8,
    5: 12,
}

Y_OFFSETS = {
    0: 0,
    1: 4,
    2: 4,
    3: 4,
    4: 8,
    5: 8,
}


def switch_map_v1(
    map_size: int, map_idx: int, position: Point2D, direction: Direction
) -> tuple[int, Point2D, Direction]:
    if map_idx == 0:
        next_map_idx = {
            Direction.RIGHT: 0,
            Direction.DOWN: 3,
            Direction.LEFT: 0,
            Direction.UP: 4,
        }[direction]
    elif map_idx == 1:
        next_map_idx = {
            Direction.RIGHT: 2,
            Direction.DOWN: 1,
            Direction.LEFT: 3,
            Direction.UP: 1,
        }[direction]
    elif map_idx == 2:
        next_map_idx = {
            Direction.RIGHT: 3,
            Direction.DOWN: 2,
            Direction.LEFT: 1,
            Direction.UP: 2,
        }[direction]
    elif map_idx == 3:
        next_map_idx = {
            Direction.RIGHT: 1,
            Direction.DOWN: 4,
            Direction.LEFT: 2,
            Direction.UP: 0,
        }[direction]
    elif map_idx == 4:
        next_map_idx = {
            Direction.RIGHT: 5,
            Direction.DOWN: 0,
            Direction.LEFT: 5,
            Direction.UP: 3,
        }[direction]
    elif map_idx == 5:
        next_map_idx = {
            Direction.RIGHT: 4,
            Direction.DOWN: 5,
            Direction.LEFT: 4,
            Direction.UP: 5,
        }[direction]
    else:
        assert 0
    next_position = {
        Direction.RIGHT: lambda p: Point2D(0, p.y),
        Direction.DOWN: lambda p: Point2D(p.x, 0),
        Direction.LEFT: lambda p: Point2D(map_size - 1, p.y),
        Direction.UP: lambda p: Point2D(p.x, map_size - 1),
    }[direction](position)
    return next_map_idx, next_position, direction
