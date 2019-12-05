import os
from typing import List, Tuple, NamedTuple


def apply_command(lst: List[Tuple[int, int]], command: str) -> None:
    previous = lst[-1]

    direction = command[0]
    amount = int(command[1:])

    if direction == 'u':
        def action(i):
            lst.append((previous[0] + i, previous[1]))
    elif direction == 'r':
        def action(i):
            lst.append((previous[0], previous[1] + i))
    elif direction == 'd':
        def action(i):
            lst.append((previous[0] - i, previous[1]))
    elif direction == 'l':
        def action(i):
            lst.append((previous[0], previous[1] - i))
    else:
        raise Exception('Direction {} not supported'.format(direction))

    for i in range(amount):
        action(i + 1)


def build_wire(text: str) -> List[Tuple[int, int]]:
    commands = text.strip().lower().split(',')

    out = [(0, 0)]

    for command in commands:
        apply_command(out, command)

    out.pop(0)

    return out


class BoundingBox(NamedTuple):
    x_max: int
    x_min: int
    y_max: int
    y_min: int


def get_bounding_box(wire: List[Tuple[int, int]]) -> BoundingBox:
    x_max = max(map(lambda x: x[0], wire))
    x_min = min(map(lambda x: x[0], wire))
    y_max = max(map(lambda x: x[1], wire))
    y_min = min(map(lambda x: x[1], wire))
    return BoundingBox(x_max=x_max, x_min=x_min, y_max=y_max, y_min=y_min)


def intersect_bounding_boxes(b1: BoundingBox, b2: BoundingBox) -> BoundingBox:
    x_max = min([b1.x_max, b2.x_max])
    x_min = max([b1.x_min, b2.x_min])
    y_max = min([b1.y_max, b2.y_max])
    y_min = max([b1.y_min, b2.y_min])
    return BoundingBox(x_max=x_max, x_min=x_min, y_max=y_max, y_min=y_min)


def get_distance_to_point(point: Tuple[int, int], wire: List[Tuple[int, int]]) -> int:
    for idx, wire_point in enumerate(wire):
        if point == wire_point:
            return idx + 1
    raise Exception("Point is not on wire")


if __name__ == "__main__":
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, 'input.txt')

    with open(input_path) as f:
        wire_1_raw = f.readline()
        wire_2_raw = f.readline()

        wire_1 = build_wire(wire_1_raw)
        wire_2 = build_wire(wire_2_raw)

        bounding_1 = get_bounding_box(wire_1)
        bounding_2 = get_bounding_box(wire_2)
        bounding = intersect_bounding_boxes(bounding_1, bounding_2)

        def filter_func(x: Tuple[int, int]) -> bool:
            return x[0] < bounding.x_max and x[0] > bounding.x_min and x[1] < bounding.y_max and x[1] > bounding.y_min

        filtered_wire_1 = list(filter(filter_func, wire_1))
        filtered_wire_2 = list(filter(filter_func, wire_2))

        common = [x for x in filtered_wire_1 if x in filtered_wire_2]
        manhattan = list(map(lambda x: abs(x[0]) + abs(x[1]), common))

        print('Part 1')
        print('Distance = {}'.format(min(manhattan)))

        min_distance = -1

        for point in common:
            wire_1_distance = get_distance_to_point(point, wire_1)
            wire_2_distance = get_distance_to_point(point, wire_2)

            if min_distance < 0 or (wire_1_distance + wire_2_distance < min_distance):
                min_distance = wire_1_distance + wire_2_distance

        print('Part 2')
        print('Distance = {}'.format(min_distance))
