import os
import itertools
import time


class ConsoleDrawer():
    def __init__(self, key):
        self._is_windows = os.name == 'nt'
        self._key = key

    def draw(self, data):
        self._clear()
        x_min, x_max = self._get_range([k[0] for k in data.keys()])
        y_min, y_max = self._get_range([k[1] for k in data.keys()])
        for y in range(y_max, y_min - 1, -1):
            line = self._build_line(y, data, x_min, x_max)
            print(line)

    def animate(self, datas, dt=0.25):
        for data in datas:
            self.draw(data)
            time.sleep(dt)

    def _get_range(self, values):
        return min(values), max(values)

    def _build_line(self, y, data, x_min, x_max):
        line = []
        for x in range(x_min, x_max + 1):
            if (x, y) in data:
                line.append(self._key[data[(x, y)]])
            else:
                line.append(' ')
        return ''.join(line)

    def _clear(self):
        if self._is_windows:
            os.system('cls')
        else:
            os.system('clear')
