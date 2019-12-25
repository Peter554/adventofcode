import os
import random
import asyncio

from intcode import IntCode
from consoledrawer import ConsoleDrawer


class Arcade():
    def __init__(self, raw_code):
        raw_code = '2' + raw_code[1:]
        self._computer = IntCode(raw_code, asyncio.Queue())

    async def run(self):
        self._stopped = False
        self._d = {}
        self._score = None
        self._ball_history = []
        tasks = []
        tasks.append(asyncio.create_task(self._computer.run()))
        tasks.append(asyncio.create_task(self._draw()))
        tasks.append(asyncio.create_task(self._receive_input()))
        await asyncio.gather(*tasks)

    async def stop(self):
        self._stopped = True

    async def _draw(self):
        while not self._stopped:
            try:
                x = await asyncio.wait_for(self._computer.output_queue.get(), 1)
                y = await asyncio.wait_for(self._computer.output_queue.get(), 1)
                tile_id = await asyncio.wait_for(self._computer.output_queue.get(), 1)
            except asyncio.TimeoutError:
                break
            if x == -1 and y == 0:
                self._score = tile_id
            else:
                self._d[(x, y)] = tile_id
                if tile_id == 4:
                    self._ball_history.append((x, y))
            draw_arcade(self._d, self._score)

    async def _receive_input(self):
        while not self._stopped:
            choice = random.choice([0, 1, -1])
            self._computer.input_queue.put_nowait(choice)
            await asyncio.sleep(0.01)


def draw_arcade(arcade, score):
    key = {0: ' ', 1: '#', 2: '£', 3: '=', 4: 'o'}
    drawer = ConsoleDrawer(key)
    drawer.draw(arcade)
    print(f'Score = {score}')


async def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, 'input.txt')
    with open(input_path) as f:
        raw_code = f.readline()
        arcade = Arcade(raw_code)
        await arcade.run()

if __name__ == "__main__":
    asyncio.run(main())
