from __future__ import annotations

import dataclasses
import re
import itertools
from typing import Optional


@dataclasses.dataclass(frozen=True)
class Instruction:
    state: str
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int


@dataclasses.dataclass(frozen=True)
class Cuboid:
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int

    @classmethod
    def from_instruction(cls, i: Instruction) -> Cuboid:
        return Cuboid(
            x_min=i.x_min,
            x_max=i.x_max,
            y_min=i.y_min,
            y_max=i.y_max,
            z_min=i.z_min,
            z_max=i.z_max,
        )

    @property
    def is_valid(self) -> bool:
        return (
            self.x_min <= self.x_max
            and self.y_min <= self.y_max
            and self.z_min <= self.z_max
        )

    @property
    def size(self) -> int:
        return (
            (self.x_max - self.x_min + 1)
            * (self.y_max - self.y_min + 1)
            * (self.z_max - self.z_min + 1)
        )

    def intersection(self, other: Cuboid) -> Optional[Cuboid]:
        x_min = max([self.x_min, other.x_min])
        x_max = min([self.x_max, other.x_max])
        y_min = max([self.y_min, other.y_min])
        y_max = min([self.y_max, other.y_max])
        z_min = max([self.z_min, other.z_min])
        z_max = min([self.z_max, other.z_max])
        cuboid = Cuboid(
            x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max, z_min=z_min, z_max=z_max
        )
        return cuboid if cuboid.is_valid else None

    def __sub__(self, other: Cuboid) -> frozenset[Cuboid]:
        if not self.intersection(other):
            return frozenset([self])
        cuboids = {
            Cuboid(
                x_min=self.x_min,
                x_max=other.x_min - 1,
                y_min=self.y_min,
                y_max=self.y_max,
                z_min=self.z_min,
                z_max=self.z_max,
            ),
            Cuboid(
                x_min=other.x_max + 1,
                x_max=self.x_max,
                y_min=self.y_min,
                y_max=self.y_max,
                z_min=self.z_min,
                z_max=self.z_max,
            ),
            Cuboid(
                x_min=max([other.x_min, self.x_min]),
                x_max=min([other.x_max, self.x_max]),
                y_min=self.y_min,
                y_max=other.y_min - 1,
                z_min=self.z_min,
                z_max=self.z_max,
            ),
            Cuboid(
                x_min=max([other.x_min, self.x_min]),
                x_max=min([other.x_max, self.x_max]),
                y_min=other.y_max + 1,
                y_max=self.y_max,
                z_min=self.z_min,
                z_max=self.z_max,
            ),
            Cuboid(
                x_min=max([other.x_min, self.x_min]),
                x_max=min([other.x_max, self.x_max]),
                y_min=max([other.y_min, self.y_min]),
                y_max=min([other.y_max, self.y_max]),
                z_min=self.z_min,
                z_max=other.z_min - 1,
            ),
            Cuboid(
                x_min=max([other.x_min, self.x_min]),
                x_max=min([other.x_max, self.x_max]),
                y_min=max([other.y_min, self.y_min]),
                y_max=min([other.y_max, self.y_max]),
                z_min=other.z_max + 1,
                z_max=self.z_max,
            ),
        }
        return frozenset(c for c in (*cuboids,) if c.is_valid)


def part_1(file_path: str) -> int:
    with open(file_path, "r") as f:
        lines = f.read().splitlines()

    instructions: tuple[Instruction, ...] = ()
    for line in lines:
        match = re.match(
            r"^(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)$", line
        )
        assert match
        instructions = (
            *instructions,
            Instruction(
                state=match.group(1),
                x_min=int(max([int(match.group(2)), -50])),
                x_max=int(min([int(match.group(3)), 50])),
                y_min=int(max([int(match.group(4)), -50])),
                y_max=int(min([int(match.group(5)), 50])),
                z_min=int(max([int(match.group(6)), -50])),
                z_max=int(min([int(match.group(7)), 50])),
            ),
        )

    states = {}
    for x, y, z in itertools.product(
        range(-50, 51),
        range(-50, 51),
        range(-50, 51),
    ):
        states[(x, y, z)] = False

    for i in instructions:
        for x, y, z in itertools.product(
            range(i.x_min, i.x_max + 1),
            range(i.y_min, i.y_max + 1),
            range(i.z_min, i.z_max + 1),
        ):
            if i.state == "on":
                states[(x, y, z)] = True
            else:
                states[(x, y, z)] = False

    return sum(states.values())


def part_2(file_path: str) -> int:
    with open(file_path, "r") as f:
        lines = f.read().splitlines()

    instructions: tuple[Instruction, ...] = ()
    for line in lines:
        match = re.match(
            r"^(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)$", line
        )
        assert match
        instructions = (
            *instructions,
            Instruction(
                state=match.group(1),
                x_min=int(match.group(2)),
                x_max=int(match.group(3)),
                y_min=int(match.group(4)),
                y_max=int(match.group(5)),
                z_min=int(match.group(6)),
                z_max=int(match.group(7)),
            ),
        )

    on_cuboids: set[Cuboid] = set()
    for instruction in instructions:
        cuboid = Cuboid.from_instruction(instruction)
        next_on_cuboids: set[Cuboid] = set()
        if instruction.state == "on":
            next_on_cuboids = {cuboid}
        for on_cuboid in on_cuboids:
            next_on_cuboids.update(on_cuboid - cuboid)
        on_cuboids = next_on_cuboids
    return sum([c.size for c in on_cuboids])
