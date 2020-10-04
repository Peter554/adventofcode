import functools
import math


class Fft:
    _base_pattern = (0, 1, 0, -1)

    def __init__(self, raw_code):
        self._state = tuple([int(i) for i in list(raw_code)])

    def advance(self):
        next = []
        length = len(self._state)
        for i in range(length):
            pattern = Fft.get_pattern(i + 1, length)
            value = Fft.get_value(self._state, pattern)
            next.append(value)
        self._state = tuple(next)

    def advance_n(self, n):
        for i in range(n):
            self.advance()

    def get_state(self):
        return "".join((f"{x}" for x in self._state))

    @staticmethod
    def get_pattern(dilation, length):
        base = []
        for p in Fft._base_pattern:
            for _ in range(dilation):
                base.append(p)
        base = [*base[1:], base[0]]
        base = base * math.ceil(length / len(base))
        base = base[:length]
        return tuple(base)

    @staticmethod
    def get_value(state, pattern):
        value = 0
        for idx in range(len(state)):
            value += state[idx] * pattern[idx]
        return abs(value) % 10
