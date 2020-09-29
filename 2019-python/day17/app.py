import os
import random

from intcode import IntCode
from consoledrawer import ConsoleDrawer


class Program:
    def __init__(self, raw_code):
        raw_code = "2" + raw_code[1:]
        self._computer = IntCode(raw_code, self._get_input, self._push_output)

    def run(self):
        self._inputs = self._init_inputs()
        self._dust_count = 0
        self._x = 0
        self._y = 0
        self._d = {}
        self._computer.run()
        self._draw(self._d)
        print(f"\nDust = {self._dust_count}\n")

    def _init_inputs(self):
        raw = [
            ["A", "B", "A", "B", "C", "C", "B", "C", "B", "A"],
            ["R", 12, "L", 8, "R", 12],
            ["R", 8, "R", 6, "R", 6, "R", 8],
            ["R", 8, "L", 8, "R", 8, "R", 4, "R", 4],
            ["n"],
        ]
        out = []
        for row in raw:
            for s in row:
                if isinstance(s, int):
                    for o in str(s):
                        out.append(ord(o))
                else:
                    out.append(ord(s))
                out.append(ord(","))
            out.pop()
            out.append(ord("\n"))
        return out

    def _get_input(self):
        nxt = self._inputs.pop(0)
        return nxt

    def _push_output(self, value):
        if value > 128:
            self._dust_count = value
            return
        if value == 10:
            self._y -= 1
            self._x = 0
        else:
            self._d[(self._x, self._y)] = value
            self._x += 1

    def _draw(self, d):
        key = {i: str(chr(i)) for i in range(128)}
        drawer = ConsoleDrawer(key)
        drawer.draw(d)

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
        return set(
            [
                (p[0] + 1, p[1]),
                (p[0] - 1, p[1]),
                (p[0], p[1] + 1),
                (p[0], p[1] - 1),
            ]
        )


if __name__ == "__main__":
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, "input.txt")
    with open(input_path) as f:
        raw_code = f.readline()
        program = Program(raw_code)
        program.run()
