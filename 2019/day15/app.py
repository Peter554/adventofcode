import os
import random
import asyncio

from intcode import IntCode


async def find_oxygen(raw_code):
    computer = IntCode(raw_code, asyncio.Queue())
    computer_task = asyncio.create_task(computer.run())
    position = (0, 0)
    walls = set()
    oxygen = None
    path = set()
    while True:
        choice = random.choice([1, 2, 3, 4])
        candidate = update_position(position, choice)
        if candidate in walls:
            continue
        await computer.input_queue.put(choice)
        output = await computer.output_queue.get()
        assert_valid_output(output)
        if output == 0:
            walls.add(candidate)
        else:
            if candidate in path:
                path.remove(position)
            position = candidate
            path.add(position)
        if output == 2:
            oxygen = position
            break
    return oxygen, path


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


def assert_valid_output(output):
    if not (output in [0, 1, 2]):
        raise Exception(f'Unexpected output {output}')


async def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, 'input.txt')
    with open(input_path) as f:
        raw_code = f.readline()
        print('Part 1')
        oxygen, path = await find_oxygen(raw_code)
        print(f'Steps = {len(path)}')

if __name__ == "__main__":
    asyncio.run(main())
