import os
import asyncio

from ensemble import Ensemble


async def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, "input.txt")
    with open(input_path) as f:
        raw_code = f.readline()
        e = Ensemble(raw_code)
        await e.run()


if __name__ == "__main__":
    asyncio.run(main())
