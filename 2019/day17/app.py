import os
import random

from intcode import IntCode
from consoledrawer import ConsoleDrawer


class Program():
    def __init__(self, raw_code):
        self._computer = IntCode(raw_code, self._get_input, self._push_output)

    def run(self):
        self._x = 0
        self._y = 0
        self._d = {}
        self._computer.run()
        alignment = self._get_alignment()
        print(f'Alignment = {alignment}')

    def _get_input(self):
        raise Exception('Not implemented')

    def _push_output(self, value):
        if value == 10:
            self._y += 1
            self._x = 0
        else:
            self._d[(self._x, self._y)] = value
            self._x += 1

    def _draw(self):
        key = {35: '#', 46: '.'}
        drawer = ConsoleDrawer(key)
        drawer.draw(self._d)

    def _get_alignment(self):
        out = 0
        scaffolds = set([k for k, v in self._d.items() if v == 35])
        for p in scaffolds:
            neighbors = self._get_neighbors(p)
            if len(scaffolds.intersection(neighbors)) == 4:
                x, y = p
                out += x * y
        return out

    def _get_neighbors(self, p):
        return set([
            (p[0]+1, p[1]),
            (p[0]-1, p[1]),
            (p[0], p[1]+1),
            (p[0], p[1]-1),
        ])


if __name__ == "__main__":
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, 'input.txt')
    with open(input_path) as f:
        raw_code = f.readline()
        program = Program(raw_code)
        program.run()
