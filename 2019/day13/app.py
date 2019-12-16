import os
import random
import asyncio

from intcode import IntCode


async def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, 'input.txt')
    with open(input_path) as f:
        raw_code = f.readline()
        print('Part 1')
        print(f'Steps = ')

if __name__ == "__main__":
    asyncio.run(main())
