import dataclasses
import heapq
import functools
from typing import Literal, Union, Optional

AmphipodType = Union[Literal["A"], Literal["B"], Literal["C"], Literal["D"]]


@dataclasses.dataclass(frozen=True)
class State:
    A: tuple[AmphipodType, ...]
    B: tuple[AmphipodType, ...]
    C: tuple[AmphipodType, ...]
    D: tuple[AmphipodType, ...]
    H: tuple[
        Optional[AmphipodType],
        Optional[AmphipodType],
        Optional[AmphipodType],
        Optional[AmphipodType],
        Optional[AmphipodType],
        Optional[AmphipodType],
        Optional[AmphipodType],
    ]

    def __str__(self) -> str:
        A = [x if x else "." for x in self.A + (".",) * (4 - len(self.A))]
        B = [x if x else "." for x in self.B + (".",) * (4 - len(self.B))]
        C = [x if x else "." for x in self.C + (".",) * (4 - len(self.C))]
        D = [x if x else "." for x in self.D + (".",) * (4 - len(self.D))]
        H = [x if x else "." for x in self.H]
        return f"""#############
#{H[0]}{H[1]}.{H[2]}.{H[3]}.{H[4]}.{H[5]}{H[6]}#
###{A[3]}#{B[3]}#{C[3]}#{D[3]}###
  #{A[2]}#{B[2]}#{C[2]}#{D[2]}#
  #{A[1]}#{B[1]}#{C[1]}#{D[1]}#
  #{A[0]}#{B[0]}#{C[0]}#{D[0]}#
  #########
"""


sample = State(
    A=("A", "D", "D", "B"),
    B=("D", "B", "C", "C"),
    C=("C", "A", "B", "B"),
    D=("A", "C", "A", "D"),
    H=(None, None, None, None, None, None, None),
)

puzzle = State(
    A=("C", "D", "D", "B"),
    B=("D", "B", "C", "C"),
    C=("D", "A", "B", "A"),
    D=("A", "C", "A", "B"),
    H=(None, None, None, None, None, None, None),
)

target = State(
    A=("A", "A", "A", "A"),
    B=("B", "B", "B", "B"),
    C=("C", "C", "C", "C"),
    D=("D", "D", "D", "D"),
    H=(None, None, None, None, None, None, None),
)


@functools.cache
def move_cost(
    room: AmphipodType, hallway_idx: int, room_position: int, amphipod: AmphipodType
) -> int:
    steps = {
        "A": {
            0: 3,
            1: 2,
            2: 2,
            3: 4,
            4: 6,
            5: 8,
            6: 9,
        },
        "B": {
            0: 5,
            1: 4,
            2: 2,
            3: 2,
            4: 4,
            5: 6,
            6: 7,
        },
        "C": {
            0: 7,
            1: 6,
            2: 4,
            3: 2,
            4: 2,
            5: 4,
            6: 5,
        },
        "D": {
            0: 9,
            1: 8,
            2: 6,
            3: 4,
            4: 2,
            5: 2,
            6: 3,
        },
    }[room][hallway_idx]
    steps += 3 - room_position
    cost_factor = {
        "A": 1,
        "B": 10,
        "C": 100,
        "D": 1000,
    }[amphipod]
    return steps * cost_factor


def move_to_hallway(
    d: State, room: AmphipodType, hallway_idx: int
) -> tuple[int, State]:
    room_amphipods = list(getattr(d, room))
    room_position = len(room_amphipods) - 1
    hallway = list(d.H)
    amphipod = room_amphipods.pop()
    hallway[hallway_idx] = amphipod
    cost = move_cost(room, hallway_idx, room_position, amphipod)
    return (
        cost,
        State(
            **{  # type:ignore
                "A": d.A,
                "B": d.B,
                "C": d.C,
                "D": d.D,
                "H": tuple(hallway),
                room: tuple(room_amphipods),
            }
        ),
    )


def move_to_room(
    d: State, amphipod: AmphipodType, hallway_idx: int
) -> tuple[int, State]:
    room_amphipods = list(getattr(d, amphipod))
    room_position = len(room_amphipods)
    hallway = list(d.H)
    room_amphipods.append(amphipod)
    hallway[hallway_idx] = None
    cost = move_cost(amphipod, hallway_idx, room_position, amphipod)
    return (
        cost,
        State(
            **{  # type:ignore
                "A": d.A,
                "B": d.B,
                "C": d.C,
                "D": d.D,
                "H": tuple(hallway),
                amphipod: tuple(room_amphipods),
            }
        ),
    )


def available_to_move_into_hallway(d: State, room: AmphipodType) -> tuple[int, ...]:
    if set(getattr(d, room)) == {room} or len(getattr(d, room)) == 0:
        return ()
    available = []
    left_idx = {
        "A": 1,
        "B": 2,
        "C": 3,
        "D": 4,
    }[room]
    idx = left_idx
    while idx >= 0 and d.H[idx] is None:
        available.append(idx)
        idx -= 1
    idx = left_idx + 1
    while idx <= len(d.H) - 1 and d.H[idx] is None:
        available.append(idx)
        idx += 1
    return tuple(available)


def available_to_move_into_room(d: State, room: AmphipodType) -> tuple[int, ...]:
    if set(getattr(d, room)).union({room}) > {room} or len(getattr(d, room)) == 4:
        return ()
    available = []
    left_idx = {
        "A": 1,
        "B": 2,
        "C": 3,
        "D": 4,
    }[room]
    idx = left_idx
    while idx >= 0 and d.H[idx] is None:
        idx -= 1
    if idx >= 0 and d.H[idx] == room:
        available.append(idx)
    idx = left_idx + 1
    while idx <= len(d.H) - 1 and d.H[idx] is None:
        idx += 1
    if idx <= len(d.H) - 1 and d.H[idx] == room:
        available.append(idx)
    return tuple(available)


def forward_states(d: State) -> tuple[tuple[int, State], ...]:
    states = []
    rooms: tuple[AmphipodType, ...] = ("A", "B", "C", "D")
    # moves from rooms into hallway
    for room in rooms:
        for hallway_idx in available_to_move_into_hallway(d, room):
            states.append(move_to_hallway(d, room, hallway_idx))
    # moves from hallway into rooms
    for room in rooms:
        for hallway_idx in available_to_move_into_room(d, room):
            amphipod = d.H[hallway_idx]
            assert amphipod
            states.append(move_to_room(d, amphipod, hallway_idx))
    return tuple(states)


def solve(initial_state: State) -> tuple[int, tuple[State, ...]]:
    best_costs: dict[State, int] = {initial_state: 0}
    best_paths: dict[State, Optional[State]] = {initial_state: None}
    q: list[tuple[int, int, State]] = []
    i = 0
    heapq.heappush(q, (0, i, initial_state))
    while q:
        c, _, d = heapq.heappop(q)
        if d == target:
            continue
        else:
            for fc, fd in forward_states(d):
                if (fd not in best_costs or c + fc < best_costs[fd]) and (
                    target not in best_costs or c + fc < best_costs[target]
                ):
                    best_costs[fd] = c + fc
                    best_paths[fd] = d
                    i += 1
                    heapq.heappush(q, (c + fc, i, fd))

    d = target
    path = [d]
    while best_paths[d]:
        d = best_paths[d]  # type:ignore
        path.append(d)

    return best_costs[target], tuple(reversed(path))


if __name__ == "__main__":
    cost, path = solve(puzzle)
    for d in path:
        print(d)
    print(cost)
