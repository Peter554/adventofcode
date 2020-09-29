class MoonsPeriodCalculator:
    def __init__(self, serialize, moons):
        self._serialize = serialize
        self._step = 0
        self._set = set()
        self._period = None
        s = ":".join([self._serialize(m) for m in moons])
        self._set.add(s)

    def next(self, moons):
        self._step += 1
        s = ":".join([self._serialize(m) for m in moons])
        if (self._period is None) and (s in self._set):
            self._period = self._step
        self._set.add(s)
        return self._period
