from day23 import solution


def test_solve() -> None:
    cost, _ = solution.solve(solution.sample)
    assert cost == 44169
    cost, _ = solution.solve(solution.puzzle)
    assert cost == 49742
