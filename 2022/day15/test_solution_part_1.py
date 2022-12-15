import pytest

from day15.solution_part_1 import (
    solve,
    SensorReport,
    Point2D,
    xranges_overlapping,
    merge_xranges,
    merge_overlapping_xranges,
    get_forbidden_beacon_xrange,
)


@pytest.mark.parametrize(
    "sensor_report,expected_xrange",
    [
        [
            SensorReport(
                Point2D(10, 10),
                Point2D(11, 11),
            ),
            None,
        ],
        [
            SensorReport(
                Point2D(0, 2),
                Point2D(0, 0),
            ),
            None,
        ],
        [
            SensorReport(
                Point2D(0, 0),
                Point2D(2, 2),
            ),
            (-4, 4),
        ],
        [
            SensorReport(
                Point2D(0, 0),
                Point2D(-4, 0),
            ),
            (-3, 4),
        ],
        [
            SensorReport(
                Point2D(0, 0),
                Point2D(4, 0),
            ),
            (-4, 3),
        ],
        [
            SensorReport(
                Point2D(2, 2),
                Point2D(0, 0),
            ),
            (1, 4),
        ],
        [
            SensorReport(
                Point2D(-2, 6),
                Point2D(0, 0),
            ),
            (-4, -1),
        ],
    ],
)
def test_get_forbidden_beacon_xrange(sensor_report, expected_xrange):
    assert get_forbidden_beacon_xrange(sensor_report, 0) == expected_xrange


@pytest.mark.parametrize(
    "xrange1,xrange2,expect_overlapping",
    [
        [(1, 4), (5, 8), False],
        [(1, 4), (3, 8), True],
        [(1, 4), (4, 8), True],
    ],
)
def test_xranges_overlapping(xrange1, xrange2, expect_overlapping):
    assert xranges_overlapping(xrange1, xrange2) == expect_overlapping
    assert xranges_overlapping(xrange2, xrange1) == expect_overlapping


@pytest.mark.parametrize(
    "xrange1,xrange2,expected_merged_xrange",
    [
        [(1, 4), (3, 8), (1, 8)],
        [(1, 4), (4, 8), (1, 8)],
    ],
)
def test_merge_xranges(xrange1, xrange2, expected_merged_xrange):
    assert merge_xranges(xrange1, xrange2) == expected_merged_xrange
    assert merge_xranges(xrange2, xrange1) == expected_merged_xrange


@pytest.mark.parametrize(
    "xranges,expected_merged_xranges",
    [
        [
            [],
            [],
        ],
        [
            [(1, 4)],
            [(1, 4)],
        ],
        [
            [(1, 4), (5, 8)],
            [(1, 4), (5, 8)],
        ],
        [
            [(1, 4), (3, 8)],
            [(1, 8)],
        ],
        [
            [(1, 4), (4, 8)],
            [(1, 8)],
        ],
        [
            [(1, 4), (3, 8), (11, 15), (13, 17)],
            [(1, 8), (11, 17)],
        ],
        [
            [(1, 4), (3, 8), (8, 15), (13, 17)],
            [(1, 17)],
        ],
    ],
)
def test_merge_overlapping_xranges(xranges, expected_merged_xranges):
    assert merge_overlapping_xranges(xranges) == expected_merged_xranges
    assert merge_overlapping_xranges(list(reversed(xranges))) == expected_merged_xranges


def test_solve():
    assert solve("day15/sample", 10) == 26
    assert solve("day15/input", 2000000) == 4737443
