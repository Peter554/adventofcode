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
    destinations: set[TState] | None = None,
    max_cost: int | None = None,
) -> dict[TState, Path[TState]]:
    shortest_paths: dict[TState, Path[TState]] = {}
    to_visit: list[tuple[int, int, tuple[TState, ...]]] = []  # heapq
    tie_break = 0  # in case of equal cost
    heapq.heappush(to_visit, (0, tie_break, (origin,)))
    while to_visit:
        cost, _, states = heapq.heappop(to_visit)
        if max_cost is not None and cost > max_cost:
            continue
        state = states[-1]
        if state in shortest_paths:
            continue

        shortest_paths[state] = Path(cost, states)
        if (
            destinations is not None
            and destinations.intersection(shortest_paths) == destinations
        ):
            break

        for neighbor_cost, neighbor_state in get_state_transitions(state):
            tie_break += 1
            heapq.heappush(
                to_visit,
                (cost + neighbor_cost, tie_break, (*states, neighbor_state)),
            )
    return shortest_paths
