from day25 import solution


def test_base_5():
    assert solution.base_5(0) == "0"
    assert solution.base_5(1) == "1"
    assert solution.base_5(2) == "2"
    assert solution.base_5(3) == "3"
    assert solution.base_5(4) == "4"
    assert solution.base_5(5) == "10"
    assert solution.base_5(6) == "11"
    assert solution.base_5(7) == "12"
    assert solution.base_5(8) == "13"
    assert solution.base_5(9) == "14"
    assert solution.base_5(10) == "20"


def test_snafu_to_decimal():
    assert solution.SNAFU("0").decimal == 0
    assert solution.SNAFU("1").decimal == 1
    assert solution.SNAFU("2").decimal == 2
    assert solution.SNAFU("1=").decimal == 3
    assert solution.SNAFU("1-").decimal == 4
    assert solution.SNAFU("10").decimal == 5
    assert solution.SNAFU("11").decimal == 6
    assert solution.SNAFU("12").decimal == 7
    assert solution.SNAFU("2=").decimal == 8
    assert solution.SNAFU("2-").decimal == 9
    assert solution.SNAFU("20").decimal == 10


def test_decimal_to_snafu():
    assert solution.SNAFU.from_decimal(0).value == "0"
    assert solution.SNAFU.from_decimal(1).value == "1"
    assert solution.SNAFU.from_decimal(2).value == "2"
    assert solution.SNAFU.from_decimal(3).value == "1="
    assert solution.SNAFU.from_decimal(4).value == "1-"
    assert solution.SNAFU.from_decimal(5).value == "10"


def test_part_1():
    assert solution.part_1("day25/sample") == "2=-1=0"
    assert solution.part_1("day25/input") == "20=212=1-12=200=00-1"
