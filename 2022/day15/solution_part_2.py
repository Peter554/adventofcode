import re


import dataclasses
import functools

from common.point2d import Point2D


@dataclasses.dataclass(frozen=True)
class SensorReport:
    sensor: Point2D
    closest_beacon: Point2D

    @functools.cached_property
    def taxicab(self) -> int:
        return self.sensor.taxicab(self.closest_beacon)

    def permits_beacon(self, p: Point2D) -> bool:
        if p == self.closest_beacon:
            return False
        return self.sensor.taxicab(p) > self.taxicab


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


def get_beacon_candidates(sr: SensorReport, search_space: int) -> list[Point2D]:
    candidates: set[Point2D] = set()
    for dx in range(sr.taxicab + 2):
        dy = sr.taxicab + 1 - dx
        candidates.add(Point2D(sr.sensor.x + dx, sr.sensor.y + dy))
        candidates.add(Point2D(sr.sensor.x - dx, sr.sensor.y + dy))
        candidates.add(Point2D(sr.sensor.x + dx, sr.sensor.y - dy))
        candidates.add(Point2D(sr.sensor.x - dx, sr.sensor.y - dy))
    return [
        c
        for c in list(candidates)
        if 0 <= c.x <= search_space and 0 <= c.y <= search_space
    ]


def solve(file_path: str, search_space: int) -> int:
    with open(file_path) as f:
        raw_sensor_reports = [line.strip() for line in f.readlines()]
    sensor_reports = parse_sensor_reports(raw_sensor_reports)
    for sensor_report in sensor_reports:
        for beacon_candidate in get_beacon_candidates(sensor_report, search_space):
            if all(sr.permits_beacon(beacon_candidate) for sr in sensor_reports):
                return beacon_candidate.x * 4000000 + beacon_candidate.y
    assert False
