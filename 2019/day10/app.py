import os
import math
import functools


def find_best_location(raw_data):
    points = build_points(raw_data)
    counts = {}
    for point in points:
        counts[point] = count_visible(point, points)
    best_location = (-1, -1)
    best_count = 0
    for k, v in counts.items():
        if v > best_count:
            best_location = k
            best_count = v
    return best_location, best_count


def find_nth_destroyed(raw_data):
    points = build_points(raw_data)
    best_location, _ = find_best_location(raw_data)
    targets = [get_displacement(p, best_location)
               for p in points if p != best_location]
    targets.sort(key=functools.cmp_to_key(compare_func))


def build_points(raw_data):
    points = []
    for j, line in enumerate(raw_data):
        for i, char in enumerate(list(line)):
            if char == '#':
                points.append((i, j))
    return points


def count_visible(point, points):
    displacements = []
    for other in points:
        if other == point:
            continue
        displacement = get_displacement(other, point)
        if not contains(displacement, displacements):
            displacements.append(displacement)
    return len(displacements)


def get_displacement(go_to, go_from):
    dx = go_to[0] - go_from[0]
    dy = go_to[1] - go_from[1]
    return (dx, dy)


def contains(displacement, displacements):
    for v in displacements:
        if are_same_direction(displacement, v):
            return True
    return False


def are_same_direction(d_1, d_2):
    if d_1[0] * d_2[0] < 0 or d_1[1] * d_2[1] < 0:
        return False
    elif d_1[0] == 0:
        return d_2[0] == 0 and (d_1[1] == d_2[1] or d_1[1] * d_2[1] > 0)
    elif d_1[1] == 0:
        return d_2[1] == 0 and (d_1[0] == d_2[0] or d_1[0] * d_2[0] > 0)
    elif d_2[0] == 0:
        return d_1[0] == 0 and (d_1[1] == d_2[1] or d_1[1] * d_2[1] > 0)
    elif d_2[1] == 0:
        return d_1[1] == 0 and (d_1[0] == d_2[0] or d_1[0] * d_2[0] > 0)
    elif abs(d_1[0]) > abs(d_2[0]):
        factor = d_1[0] / d_2[0]
        return d_1[1] == d_2[1] * factor
    else:
        factor = d_2[0] / d_1[0]
        return d_2[1] == d_1[1] * factor


def compare_func(d_1, d_2):
    angle_1 = get_angle(d_1)
    angle_2 = get_angle(d_2)
    if not are_same_direction(d_1, d_2):
        return +1 if angle_1 > angle_2 else -1
    size_1 = get_size(d_1)
    size_2 = get_size(d_2)
    return +1 if size_1 > size_2 else -1


def get_size(d):
    return math.sqrt(d[0]**2+d[1]**2)


def get_angle(d):
    return math.atan2(d[1], d[0])


if __name__ == '__main__':
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, 'input.txt')
    with open(input_path) as f:
        raw_data = f.readlines()
        print('Part 1')
        print(f'Best location = {find_best_location(raw_data)}')
        print('Part 2')
