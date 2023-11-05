from __future__ import annotations

import dataclasses
import typing
import functools

# https://www.reddit.com/r/adventofcode/comments/rjs8rd/comment/hp5jopz/?utm_source=share&utm_medium=web2x&context=3
# Put a smiley face on a d6. You can make the smiley face point
# in six different directions, and each direction you can rotate
# the smiley face four different ways. 6 * 4 = 24.
all_rotations = (
    (),
    (2,),
    (2, 2),
    (2, 2, 2),
    #
    (0, 0),
    (0, 0, 2),
    (0, 0, 2, 2),
    (0, 0, 2, 2, 2),
    #
    (0,),
    (0, 1),
    (0, 1, 1),
    (0, 1, 1, 1),
    #
    (0, 0, 0),
    (0, 0, 0, 1),
    (0, 0, 0, 1, 1),
    (0, 0, 0, 1, 1, 1),
    #
    (1,),
    (1, 0),
    (1, 0, 0),
    (1, 0, 0, 0),
    #
    (1, 1, 1),
    (1, 1, 1, 0),
    (1, 1, 1, 0, 0),
    (1, 1, 1, 0, 0, 0),
)


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def rotate(self, axis: int) -> Point:
        if axis == 0:
            return Point(self.x, -self.z, self.y)
        elif axis == 1:
            return Point(self.z, self.y, -self.x)
        elif axis == 2:
            return Point(-self.y, self.x, self.z)
        else:
            raise Exception("invalid axis")

    @property
    def manhattan(self) -> int:
        return int(abs(self.x) + abs(self.y) + abs(self.z))


@dataclasses.dataclass(frozen=True)
class MatchTrue:
    rotation: tuple[int, ...]
    translation: Point
    match: typing.Literal[True] = True


@dataclasses.dataclass(frozen=True)
class MatchFalse:
    match: typing.Literal[False] = False


Match = typing.Union[MatchTrue, MatchFalse]


@dataclasses.dataclass(frozen=True)
class MisalignedSensor:
    beacons: frozenset[Point]

    def rotate(self, rotation: tuple[int, ...]) -> MisalignedSensor:
        beacons = set(self.beacons)
        for axis in rotation:
            beacons = {b.rotate(axis) for b in beacons}
        return MisalignedSensor(
            frozenset(beacons),
        )

    def translate(self, translation: Point) -> MisalignedSensor:
        return MisalignedSensor(
            frozenset({b + translation for b in self.beacons}),
        )

    @functools.cache
    def match(self, other: AlignedSensor) -> Match:
        for rotation in all_rotations:
            rotated_sensor = self.rotate(rotation)
            translations: set[Point] = set()
            for m in rotated_sensor.beacons:
                for m_other in other.beacons:
                    translations.add(m_other - m)
            for translation in translations:
                rotated_translated_sensor = rotated_sensor.translate(translation)
                if (
                    len(rotated_translated_sensor.beacons.intersection(other.beacons))
                    >= 12
                ):
                    return MatchTrue(rotation, translation)
        return MatchFalse()


@dataclasses.dataclass(frozen=True)
class AlignedSensor:
    beacons: frozenset[Point]
    rotation: tuple[int, ...]
    translation: Point


def solve(file_path: str) -> tuple[int, int]:
    aligned_sensors: set[AlignedSensor] = set()
    misaligned_sensors: set[MisalignedSensor] = set()
    with open(file_path, "r") as f:
        for sensor_idx, sensor_raw_data in enumerate(f.read().split("\n\n")):
            beacons: set[Point] = set()
            for line in sensor_raw_data.splitlines()[1:]:
                x_str, y_str, z_str = line.split(",")
                beacons.add(Point(int(x_str), int(y_str), int(z_str)))
            if sensor_idx == 0:
                aligned_sensors.add(
                    AlignedSensor(frozenset(beacons), (), Point(0, 0, 0))
                )
            else:
                misaligned_sensors.add(MisalignedSensor(frozenset(beacons)))

    def match_one() -> None:
        for misaligned_sensor in (*misaligned_sensors,):
            for aligned_sensor in (*aligned_sensors,):
                match = misaligned_sensor.match(aligned_sensor)
                if match.match:
                    misaligned_sensors.remove(misaligned_sensor)
                    aligned_sensors.add(
                        AlignedSensor(
                            beacons=misaligned_sensor.rotate(match.rotation)
                            .translate(match.translation)
                            .beacons,
                            rotation=match.rotation,
                            translation=match.translation,
                        )
                    )
                    return
        raise Exception("no match found")

    while misaligned_sensors:
        match_one()

    all_beacons: set[Point] = set()
    for sensor in aligned_sensors:
        all_beacons = all_beacons.union(sensor.beacons)
    n_beacons = len(all_beacons)

    max_sensor_distance = 0
    for sensor_1 in aligned_sensors:
        for sensor_2 in aligned_sensors:
            distance = (sensor_1.translation - sensor_2.translation).manhattan
            if distance > max_sensor_distance:
                max_sensor_distance = distance

    return n_beacons, max_sensor_distance
