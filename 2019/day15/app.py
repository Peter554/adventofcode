import os
import random
import asyncio

from intcode import IntCode


async def find_oxygen(raw_code):
    input_queue = asyncio.Queue()
    computer = IntCode(raw_code, input_queue)
    asyncio.create_task(computer.run())
    position = (0, 0)
    walls = set()
    oxygen = None
    visited = set()
    while True:
        choice = random.choice([1, 2, 3, 4])
        candidate = update_position(position, choice)
        if candidate in walls:
            continue
        await input_queue.put(choice)
        output = await computer.output_queue.get()
        if not (output in [0, 1, 2]):
            raise Exception(f'Unexpected output {output}')
        if output == 0:
            walls.add(candidate)
        else:
            if candidate in visited:
                visited.remove(position)
            position = candidate
            visited.add(position)
        if output == 2:
            oxygen = position
            break
    return walls, oxygen, visited


def get_minutes(walls, oxygen):
    s = set()
    s.add(oxygen)
    minutes = 0
    while True:
        start_len = len(s)
        for p in s.copy():
            for c in get_cantidates(p):
                if not (c in walls):
                    s.add(c)
        if len(s) == start_len:
            break
        minutes += 1
    return minutes


def update_position(start, choice):
    if choice == 1:
        return (start[0] + 1, start[1])
    elif choice == 2:
        return (start[0] - 1, start[1])
    elif choice == 3:
        return (start[0], start[1] - 1)
    elif choice == 4:
        return (start[0], start[1] + 1)
    else:
        raise Exception(f'Choice {choice} not supported')


def get_cantidates(p):
    return ((p[0]+1, p[1]), (p[0]-1, p[1]), (p[0], p[1]+1), (p[0], p[1] - 1))


async def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, 'input.txt')
    with open(input_path) as f:
        raw_code = f.readline()
        print('Part 1')
        walls, oxygen, visited = await find_oxygen(raw_code)
        print(f'Steps = {len(visited)}')
        print('Part 2')
        minutes = get_minutes(walls, oxygen)
        print(f'Minutes = {minutes}')

if __name__ == "__main__":
    asyncio.run(main())
