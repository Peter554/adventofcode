import os
import random
import asyncio
import matplotlib.pyplot as plt

from intcode import IntCode


async def find_oxygen(raw_code):
    input_queue = asyncio.Queue()
    computer = IntCode(raw_code, input_queue)
    asyncio.create_task(computer.run())
    position = (0, 0)
    walls = set()
    oxygen = None
    for _ in range(200000):
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
            position = candidate
        if output == 2:
            oxygen = position
    return walls, oxygen


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


def plot_1(walls, oxygen):
    grey = []
    for i in range(-20, 12):
        for j in range(-20, 12):
            grey.append((i, j))
    plt.scatter([g[0] for g in grey], [g[1] for g in grey], color='grey')
    plt.scatter([w[0] for w in walls], [w[1] for w in walls], color='blue')
    plt.scatter([0], [0], color='red')
    plt.scatter([oxygen[0]], [oxygen[1]], color='red')
    plt.show()


async def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, 'input.txt')
    with open(input_path) as f:
        raw_code = f.readline()
        print('Part 1')
        walls, oxygen = await find_oxygen(raw_code)
        plot_1(walls, oxygen)
        print('Part 2')

if __name__ == "__main__":
    asyncio.run(main())
