from __future__ import annotations

import dataclasses
import heapq
from typing import Generic, TypeVar, Callable

TState = TypeVar("TState")


@dataclasses.dataclass(frozen=True)
class Path(Generic[TState]):
    cost: int
    states: tuple[TState, ...]

    @property
    def origin(self) -> TState:
        return self.states[0]

    @property
    def destination(self) -> TState:
        return self.states[-1]


def find_shortest_paths(
    origin: TState,
    get_state_transitions: Callable[[TState], tuple[tuple[int, TState], ...]],
    *,
    max_depth: int | None = None,
) -> dict[TState, Path[TState]]:
    shortest_paths: dict[TState, Path[TState]] = {}
    to_visit: list[tuple[int, int, tuple[TState, ...], int]] = []  # heapq
    tie_break = 0  # in case of equal cost
    heapq.heappush(to_visit, (0, tie_break, (origin,), 0))
    while to_visit:
        cost, _, states, depth = heapq.heappop(to_visit)
        state = states[-1]
        if state in shortest_paths:
            continue
        if max_depth is not None and depth > max_depth:
            continue

        shortest_paths[state] = Path(cost, states)
        for neighbor_cost, neighbor_state in get_state_transitions(state):
            tie_break += 1
            heapq.heappush(
                to_visit,
                (cost + neighbor_cost, tie_break, (*states, neighbor_state), depth + 1),
            )
    return shortest_paths


def find_shortest_paths_simple(
    origin: TState,
    get_state_transitions: Callable[[TState], tuple[tuple[int, TState], ...]],
    *,
    max_depth: int | None = None,
) -> dict[TState, int]:
    shortest_paths: dict[TState, int] = {}
    to_visit: list[tuple[int, int, TState, int]] = []  # heapq
    tie_break = 0  # in case of equal cost
    heapq.heappush(to_visit, (0, tie_break, origin, 0))
    while to_visit:
        cost, _, state, depth = heapq.heappop(to_visit)
        if state in shortest_paths:
            continue
        if max_depth is not None and depth > max_depth:
            continue

        shortest_paths[state] = cost
        for neighbor_cost, neighbor_state in get_state_transitions(state):
            tie_break += 1
            heapq.heappush(
                to_visit,
                (cost + neighbor_cost, tie_break, neighbor_state, depth + 1),
            )
    return shortest_paths
