import functools
import math


class Fft():
    _base_pattern = (0, 1, 0, -1)

    def __init__(self, raw_code):
        self._state = [int(i) for i in list(raw_code)]

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
