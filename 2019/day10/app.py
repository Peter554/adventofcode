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
    displacements = set()
    for other in points:
        if other != point:
            displacements.add(get_displacement(other, point))
    return len(displacements)


def get_displacement(go_to, go_from):
    x = go_to[0] - go_from[0]
    y = go_to[1] - go_from[1]
    d = math.sqrt(x**2 + y**2)
    return (x/d, y/d)


if __name__ == '__main__':
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, 'input.txt')
    with open(input_path) as f:
        raw_data = f.readlines()
        print('Part 1')
        print(f'Best location = {find_best_location(raw_data)}')
        print('Part 2')
