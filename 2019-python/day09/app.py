import os
import asyncio

from intcode import IntCode


async def run_intcode(raw_code, inputs=[]):
    input_queue = asyncio.Queue()
    computer = IntCode(raw_code, input_queue)
    for value in inputs:
        await input_queue.put(value)
    return await computer.run()


async def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, "input.txt")

    with open(input_path) as f:
        raw_code = f.readline()
        print("Part 1")
        print(f"Keycode = {await run_intcode(raw_code, [1])}")
        print("Part 2")
        print(f"Keycode = {await run_intcode(raw_code, [2])}")


if __name__ == "__main__":
    asyncio.run(main())
