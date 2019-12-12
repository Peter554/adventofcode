
class Coordinate():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return \
            (self.x == other.x) and \
            (self.y == other.y) and \
            (self.z == other.z)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Coordinate(x, y, z)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Coordinate(x, y, z)

    def sign(self):
        x = self._sign(self.x)
        y = self._sign(self.y)
        z = self._sign(self.z)
        return Coordinate(x, y, z)

    def _sign(self, x):
        if x > 0:
            return +1
        elif x < 0:
            return -1
        else:
            return 0
