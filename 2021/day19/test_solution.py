from day19 import solution


def test_solve() -> None:
    assert solution.solve("day19/sample") == (79, 3621)
    # assert solution.solve("day19/input") == (342, 9668)  # slow :(
