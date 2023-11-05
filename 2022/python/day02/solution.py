SCORE_MAPPING = {
    "A": {
        "A": 1 + 3,
        "B": 2 + 6,
        "C": 3 + 0,
    },
    "B": {
        "A": 1 + 0,
        "B": 2 + 3,
        "C": 3 + 6,
    },
    "C": {
        "A": 1 + 6,
        "B": 2 + 0,
        "C": 3 + 3,
    },
}


def part_1(file_path: str) -> int:
    with open(file_path) as f:
        games = [line.strip().split() for line in f.readlines()]

    strategy_mapping = {
        "X": "A",
        "Y": "B",
        "Z": "C",
    }

    score = 0
    for move_p1, instruction in games:
        move_p2 = strategy_mapping[instruction]
        score += SCORE_MAPPING[move_p1][move_p2]
    return score


def part_2(file_path: str) -> int:
    with open(file_path) as f:
        games = [line.strip().split() for line in f.readlines()]

    strategy_mapping = {
        "A": {
            "X": "C",  # X: lose
            "Y": "A",  # Y: draw
            "Z": "B",  # Z: win
        },
        "B": {
            "X": "A",
            "Y": "B",
            "Z": "C",
        },
        "C": {
            "X": "B",
            "Y": "C",
            "Z": "A",
        },
    }

    score = 0
    for move_p1, instruction in games:
        move_p2 = strategy_mapping[move_p1][instruction]
        score += SCORE_MAPPING[move_p1][move_p2]
    return score
