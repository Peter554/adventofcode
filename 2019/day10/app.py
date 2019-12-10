import os
import math


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
        if are_equal(displacement, v):
            return True
    return False


def are_equal(d_1, d_2):
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


if __name__ == '__main__':
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, 'input.txt')
    with open(input_path) as f:
        raw_data = f.readlines()
        print('Part 1')
        print(f'Best location = {find_best_location(raw_data)}')
        print('Part 2')
