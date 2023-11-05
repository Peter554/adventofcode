from day07 import solution


def test_part_1():
    assert solution.part_1("day07/sample") == 95437
    assert solution.part_1("day07/input") == 1490523


def test_part_2():
    assert solution.part_2("day07/sample") == 24933642
    assert solution.part_2("day07/input") == 12390492
