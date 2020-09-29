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
    drawer = ConsoleDrawer({0: ".", 1: "#"})
    drawer.draw(results)


async def find_magic_point(raw_code):
    p = (5, 7)
    mode = "h"

    def get_next(point, mode):
        if mode == "h":
            return (point[0] + 1, point[1])
        elif mode == "v":
            return (point[0], point[1] + 1)

    while True:
        valid = await run_code(raw_code, *p) == 1
        if valid and mode == "v":
            mode = "h"
        if (not valid) and mode == "h":
            mode = "v"
        if valid and (p[0] >= 100):
            is_magic, magic = await test_rectangle(raw_code, *p)
            if is_magic:
                return magic
        p = get_next(p, mode)


async def test_rectangle(raw_code, x, y):
    points = ((x, y), (x - 99, y + 99), (x, y + 99), (x - 99, y))
    results = {}
    for point in points:
        results[point] = await run_code(raw_code, *point)
    magic = points[-1][0] * 10000 + points[-1][1]
    return len([v for v in results.values() if v == 1]) == len(points), magic


async def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, "input.txt")
    with open(input_path) as f:
        raw_code = f.readline()
        print("Part 1")
        results = await scan_area(raw_code)
        print(f"# of points = {len([v for v in results.values() if v == 1])}")
        print("Part 2")
        magic = await find_magic_point(raw_code)
        print(f"Magic = {magic}")


if __name__ == "__main__":
    asyncio.run(main())
