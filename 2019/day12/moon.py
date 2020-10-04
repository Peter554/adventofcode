import collections
import re

from coordinate import Coordinate


class Moon:
    def __init__(self, raw_data):
        self.p = self._parse_raw_data(raw_data)
        self.v = Coordinate(0, 0, 0)

    def update_velocity(self, moons):
        dv = Coordinate(0, 0, 0)
        for moon in moons:
            if moon == self:
                continue
            difference = moon.p - self.p
            dv += difference.sign()
        self.v += dv

    def update_position(self):
        self.p += self.v

    def energy(self):
        return self.potential_energy() * self.kinetic_energy()

    def potential_energy(self):
        return abs(self.p.x) + abs(self.p.y) + abs(self.p.z)

    def kinetic_energy(self):
        return abs(self.v.x) + abs(self.v.y) + abs(self.v.z)

    @staticmethod
    def _parse_raw_data(raw_data):
        r = re.compile(r"<x=(.+?),\sy=(.+?),\sz=(.+?)>")
        m = r.match(raw_data)
        return Coordinate(int(m.group(1)), int(m.group(2)), int(m.group(3)))
