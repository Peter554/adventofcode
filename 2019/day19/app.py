import os
import asyncio
import itertools

from intcode import IntCode
from consoledrawer import ConsoleDrawer


async def run_code(raw_code, x, y):
    computer = IntCode(raw_code, asyncio.Queue())
    await computer.input_queue.put(x)
    await computer.input_queue.put(y)
    return await computer.run()


async def scan_area(raw_code):
    points = itertools.product(range(50), range(50))
    results = {}
    for point in points:
        results[point] = await run_code(raw_code, *point)
    return results


def draw_results(results):
    drawer = ConsoleDrawer({0: '.', 1: '#'})
    drawer.draw(results)


async def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, 'input.txt')
    with open(input_path) as f:
        raw_code = f.readline()
        print('Part 1')
        results = await scan_area(raw_code)
        print(f'# of points = {len([v for v in results.values() if v == 1])}')

if __name__ == '__main__':
    asyncio.run(main())
