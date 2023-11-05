import collections
import functools
import itertools


def part_1(p0_position: int, p1_position: int) -> int:
    positions = [p0_position, p1_position]
    scores = [0, 0]
    next_roll = 0
    n_rolls = 0
    while True:
        for player_idx in (0, 1):
            if any(score >= 1000 for score in scores):
                return min(scores) * n_rolls
            rolls: tuple[int, ...] = ()
            for _ in range(3):
                rolls = (*rolls, next_roll)
                next_roll = (next_roll + 1) % 100
            n_rolls += 3
            positions[player_idx] = (
                positions[player_idx] + sum([roll + 1 for roll in rolls])
            ) % 10
            scores[player_idx] += positions[player_idx] + 1


def part_2(p0_position: int, p1_position: int) -> int:
    rolls_sums = tuple(
        sum(rolls) for rolls in itertools.product(range(1, 4), range(1, 4), range(1, 4))
    )

    @functools.cache
    def check_game(
        ip0: int, is0: int, ip1: int, is1: int, player_turn: int
    ) -> collections.Counter[int]:
        if is0 >= 21:
            return collections.Counter([0])
        elif is1 >= 21:
            return collections.Counter([1])

        counter = collections.Counter[int]()
        if player_turn == 0:
            p0s = tuple((ip0 + roll) % 10 for roll in rolls_sums)
            s0s = tuple(is0 + p1 + 1 for p1 in p0s)
            for p0, s0 in zip(p0s, s0s):
                counter += check_game(p0, s0, ip1, is1, 1)
        else:
            p1s = tuple((ip1 + roll) % 10 for roll in rolls_sums)
            s1s = tuple(is1 + p2 + 1 for p2 in p1s)
            for p1, s1 in zip(p1s, s1s):
                counter += check_game(ip0, is0, p1, s1, 0)
        return counter

    return max(check_game(p0_position, 0, p1_position, 0, 0).values())
