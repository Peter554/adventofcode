import os
import random
import asyncio

from intcode import IntCode


async def build_arcade(raw_code):
    d = {0: [], 1: [], 2: [], 3: [], 4: []}
    computer = IntCode(raw_code, asyncio.Queue())
    _ = await computer.run()
    while True:
        try:
            left = computer.output_queue.get_nowait()
            top = computer.output_queue.get_nowait()
            tile_id = computer.output_queue.get_nowait()
            d[tile_id].append((left, top))
        except asyncio.QueueEmpty:
            break
    return d


async def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, 'input.txt')
    with open(input_path) as f:
        raw_code = f.readline()
        d = await build_arcade(raw_code)
        print('Part 1')
        print(f'Blocks = {len(d[2])}')

if __name__ == "__main__":
    asyncio.run(main())
