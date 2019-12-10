class LargeArray():
    def __init__(self, initializer=[]):
        self._dict = {}
        for idx, value in enumerate(initializer):
            self._dict[idx] = value

    def __getitem__(self, idx):
        try:
            return self._dict[idx]
        except KeyError:
            return 0

    def __setitem__(self, idx, value):
        self._dict[idx] = value
