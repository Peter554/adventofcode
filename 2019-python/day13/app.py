import os
import random

from intcode import IntCode
from consoledrawer import ConsoleDrawer


class Arcade():
    def run(self, raw_code):
        raw_code = '2' + raw_code[1:]
        self._arcade = {}
        self._score = None
        self._outputs = []
        computer = IntCode(raw_code, self._handle_input, self._handle_output)
        computer.run()

    def _handle_input(self):
        inverted = {v: k for k, v in self._arcade.items()}
        if 3 in inverted and 4 in inverted:
            paddle = inverted[3]
            ball = inverted[4]
            if paddle[0] == ball[0]:
                return 0
            elif paddle[0] < ball[0]:
                return +1
            elif paddle[0] > ball[0]:
                return -1
        return 0

    def _handle_output(self, value):
        self._outputs.append(value)
        if len(self._outputs) == 3:
            x, y, tile_id = self._outputs
            if x == -1 and y == 0:
                self._score = tile_id
            else:
                self._arcade[(x, y)] = tile_id
            self._outputs = []
            draw_arcade(self._arcade, self._score)


def draw_arcade(arcade, score):
    key = {0: ' ', 1: '#', 2: '£', 3: '=', 4: 'o'}
    drawer = ConsoleDrawer(key)
    drawer.draw(arcade)
    print(f'Score = {score}')


if __name__ == "__main__":
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, 'input.txt')
    with open(input_path) as f:
        raw_code = f.readline()
        arcade = Arcade()
        arcade.run(raw_code)
