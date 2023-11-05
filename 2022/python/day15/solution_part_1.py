import re

import functools
import dataclasses

from common.point2d import Point2D


@dataclasses.dataclass(frozen=True)
class SensorReport:
    sensor: Point2D
    closest_beacon: Point2D

    @functools.cached_property
    def taxicab(self) -> int:
        return self.sensor.taxicab(self.closest_beacon)


def parse_sensor_reports(
    raw_sensor_reports: list[str],
) -> list[SensorReport]:
    sensor_reports: list[SensorReport] = []
    for raw_sensor_report in raw_sensor_reports:
        match = re.match(
            r"Sensor at x=([\d-]+), y=([\d-]+): closest beacon is at x=([\d-]+), y=([\d-]+)",
            raw_sensor_report,
        )
        assert match is not None
        sensor = Point2D(int(match.group(1)), int(match.group(2)))
        closest_beacon = Point2D(int(match.group(3)), int(match.group(4)))
        sensor_reports.append(SensorReport(sensor, closest_beacon))
    return sensor_reports


Xrange = tuple[int, int]


def get_forbidden_beacon_xrange(sr: SensorReport, y: int) -> Xrange | None:
    p = Point2D(sr.sensor.x, y)
    d = sr.taxicab - sr.sensor.taxicab(p)
    if d < 0:
        return None
    elif d == 0 and p == sr.closest_beacon:
        return None
    elif sr.closest_beacon.y == y:
        if sr.closest_beacon.x == sr.sensor.x - d:
            return sr.sensor.x - d + 1, sr.sensor.x + d
        else:
            return sr.sensor.x - d, sr.sensor.x + d - 1
    else:
        return sr.sensor.x - d, sr.sensor.x + d


def xranges_overlapping(xrange1: Xrange, xrange2: Xrange) -> bool:
    if xrange1[0] <= xrange2[0]:
        return xrange1[1] >= xrange2[0]
    else:
        return xrange2[1] >= xrange1[0]


def merge_xranges(xrange1: Xrange, xrange2: Xrange) -> Xrange:
    return min(xrange1[0], xrange2[0]), max(xrange1[1], xrange2[1])


def merge_overlapping_xranges(xranges: list[Xrange]) -> list[Xrange]:
    if len(xranges) <= 1:
        return xranges
    xranges = sorted(xranges)
    stack = [xranges[0]]
    for xrange in xranges[1:]:
        if xranges_overlapping(stack[-1], xrange):
            stack.append(merge_xranges(stack.pop(), xrange))
        else:
            stack.append(xrange)
    return stack


def solve(file_path: str, y: int) -> int:
    with open(file_path) as f:
        raw_sensor_reports = [line.strip() for line in f.readlines()]
    sensor_reports = parse_sensor_reports(raw_sensor_reports)
    forbidden_beacon_xranges: list[Xrange] = []
    for sr in sensor_reports:
        if (sensor_forbidden_xrange := get_forbidden_beacon_xrange(sr, y)) is not None:
            forbidden_beacon_xranges.append(sensor_forbidden_xrange)
    forbidden_beacon_xranges = merge_overlapping_xranges(forbidden_beacon_xranges)
    sum_forbidden = 0
    for forbidden_beacon_xrange in forbidden_beacon_xranges:
        x_min, x_max = forbidden_beacon_xrange
        sum_forbidden += x_max - x_min + 1
    return sum_forbidden
