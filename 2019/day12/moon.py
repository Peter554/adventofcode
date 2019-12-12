import collections
import re


def sign(x):
    if x > 0:
        return +1
    elif x < 0:
        return -1
    else:
        return 0


class Coordinate():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

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

    def truncate(self):
        x = sign(self.x)
        y = sign(self.y)
        z = sign(self.z)
        return Coordinate(x, y, z)


class Moon():
    def __init__(self, raw_data):
        self.p = self._parse_raw_data(raw_data)
        self.v = Coordinate(0, 0, 0)

    def update_velocity(self, moons):
        dv = Coordinate(0, 0, 0)
        for moon in moons:
            if moon == self:
                continue
            difference = moon.p - self.p
            dv += difference.truncate()
        self.v += dv

    def update_position(self):
        self.p += self.v

    def energy(self):
        return self.potential_energy() + self.kinetic_energy()

    def potential_energy(self):
        return abs(self.p.x) + abs(self.p.y) + abs(self.p.z)

    def kinetic_energy(self):
        return abs(self.v.x) + abs(self.v.y) + abs(self.v.z)

    @staticmethod
    def _parse_raw_data(raw_data):
        r = re.compile(r'<x=(.+?),\sy=(.+?),\sz=(.+?)>')
        m = r.match(raw_data)
        return Coordinate(int(m.group(1)), int(m.group(2)), int(m.group(3)))
