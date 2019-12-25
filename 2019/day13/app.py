import os
import random
import asyncio

from intcode import IntCode
from consoledrawer import ConsoleDrawer


class ArcadeController():
    def __init__(self, arcade):
        self._arcade = arcade

    async def get(self):
        inverted = {v: k for k, v in self._arcade.state.items()}
        if 3 in inverted:
            print(inverted)
        if 3 in inverted and 4 in inverted:
            paddle = inverted[3]
            ball = inverted[4]
            if paddle[0] == ball[0]:
                return 0
            elif paddle[0] < ball[0]:
                return -1
            elif paddle[0] > ball[0]:
                return +1
        return 0


class Arcade():
    def __init__(self, raw_code):
        raw_code = '2' + raw_code[1:]
        contoller = ArcadeController(self)
        self._computer = IntCode(raw_code, contoller)
        self._d = {}
        self._score = None

    @property
    def state(self):
        return self._d

    async def run(self):
        self._stopped = False
        self._d = {}
        self._score = None
        tasks = []
        tasks.append(asyncio.create_task(self._computer.run()))
        tasks.append(asyncio.create_task(self._draw()))
        await asyncio.gather(*tasks)

    async def stop(self):
        self._stopped = True

    async def _draw(self):
        while not self._stopped:
            try:
                await asyncio.sleep(0.01)
                x = await asyncio.wait_for(self._computer.output_queue.get(), 1)
                y = await asyncio.wait_for(self._computer.output_queue.get(), 1)
                tile_id = await asyncio.wait_for(self._computer.output_queue.get(), 1)
            except asyncio.TimeoutError:
                break
            if x == -1 and y == 0:
                self._score = tile_id
            else:
                self._d[(x, y)] = tile_id
            draw_arcade(self._d, self._score)


def draw_arcade(arcade, score):
    key = {0: ' ', 1: '#', 2: '£', 3: '=', 4: 'o'}
    # drawer = ConsoleDrawer(key)
    # drawer.draw(arcade)
    # print(f'Score = {score}')


async def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, 'input.txt')
    with open(input_path) as f:
        raw_code = f.readline()
        arcade = Arcade(raw_code)
        await arcade.run()

if __name__ == "__main__":
    asyncio.run(main())
