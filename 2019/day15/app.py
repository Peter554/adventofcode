import os
import random
import asyncio
import matplotlib.pyplot as plt

from explorer import Explorer


def find_shortest_path_to_oxygen(paths, oxygen):
    paths = tuple(p for p in paths if oxygen in p)
    path_lengths = tuple(p.index(oxygen) for p in paths)
    return min(path_lengths)


def find_minutes_to_fill(walls, oxygen):
    visited = set([oxygen])
    minutes = 0
    while True:
        start_len = len(visited)
        for p in visited.copy():
            neighbors = get_neighbors(p, walls)
            for n in neighbors:
                visited.add(n)
        minutes += 1
        if len(visited) == start_len:
            break
    return minutes


def get_neighbors(p, walls):
    out = [
        (p[0]+1, p[1]),
        (p[0]-1, p[1]),
        (p[0], p[1]+1),
        (p[0], p[1]-1),
    ]

    return [o for o in out if o not in walls]


async def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, 'input.txt')
    with open(input_path) as f:
        raw_code = f.readline()
        print('Part 1')
        explorer = Explorer(raw_code)
        paths, oxygen, walls = await explorer.explore()
        print(f'Steps = {find_shortest_path_to_oxygen(paths, oxygen)}')
        print('Part 2')
        print(f'Minutes = {find_minutes_to_fill(walls, oxygen)}')

if __name__ == "__main__":
    asyncio.run(main())
