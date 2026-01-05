from __future__ import annotations

import heapq
import itertools
from dataclasses import dataclass
from pathlib import Path


def part_1(input: Path) -> int:
    start, end, walls = parse_input(input)
    lowest_scores = find_lowest_scores(start, end, walls)
    return min([score for state, score in lowest_scores.items() if state.p == end])


def part_2(input: Path) -> int:
    start, end, walls = parse_input(input)
    lowest_scores = find_lowest_scores(start, end, walls)

    end_state, _ = min(
        [(state, score) for state, score in lowest_scores.items() if state.p == end],
        key=lambda x: x[1],
    )
    states: set[State] = set()
    q = [end_state]
    while q:
        state = q.pop(0)
        states.add(state)

        if (
            lowest_scores.get(State(state.p, CLOCKWISE[state.d]))
            == lowest_scores[state] - 1000
        ):
            q.append(State(state.p, CLOCKWISE[state.d]))

        if (
            lowest_scores.get(State(state.p, ANTICLOCKWISE[state.d]))
            == lowest_scores[state] - 1000
        ):
            q.append(State(state.p, ANTICLOCKWISE[state.d]))

        if (
            lowest_scores.get(State(state.p - state.d, state.d))
            == lowest_scores[state] - 1
        ):
            q.append(State(state.p - state.d, state.d))

    return len({state.p for state in states})


def parse_input(input: Path) -> tuple[P, P, frozenset[P]]:
    start: P | None = None
    end: P | None = None
    walls: set[P] = set()
    for y, line in enumerate(input.read_text().splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                walls.add(P(x, y))
            elif c == "S":
                start = P(x, y)
            elif c == "E":
                end = P(x, y)
    assert start is not None
    assert end is not None
    return start, end, frozenset(walls)


def find_lowest_scores(start: P, end: P, walls: frozenset[P]) -> dict[State, int]:
    counter = itertools.count()
    q = [(0, next(counter), State(start, P(1, 0)))]
    scores = {}
    while q:
        score, _, state = heapq.heappop(q)
        if state in scores:
            continue

        scores[state] = score

        heapq.heappush(
            q,
            (score + 1000, next(counter), State(state.p, CLOCKWISE[state.d])),
        )
        heapq.heappush(
            q,
            (score + 1000, next(counter), State(state.p, ANTICLOCKWISE[state.d])),
        )
        if state.p + state.d not in walls:
            heapq.heappush(
                q,
                (score + 1, next(counter), State(state.p + state.d, state.d)),
            )

    return scores


@dataclass(frozen=True)
class State:
    p: P
    d: P


@dataclass(frozen=True)
class P:
    x: int
    y: int

    def __add__(self, other: P) -> P:
        return P(self.x + other.x, self.y + other.y)

    def __sub__(self, other: P) -> P:
        return P(self.x - other.x, self.y - other.y)


CLOCKWISE = {
    P(1, 0): P(0, 1),
    P(0, 1): P(-1, 0),
    P(-1, 0): P(0, -1),
    P(0, -1): P(1, 0),
}


ANTICLOCKWISE = {
    P(1, 0): P(0, -1),
    P(0, 1): P(1, 0),
    P(-1, 0): P(0, 1),
    P(0, -1): P(-1, 0),
}
