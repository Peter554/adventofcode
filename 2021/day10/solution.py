import statistics


bracket_map = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

corrupted_score_map = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

incomplete_score_map = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def part_1(file_path: str) -> int:
    with open(file_path, "r") as f:
        lines = f.read().splitlines()
    syntax_score = 0
    for line in lines:
        stack = []
        for char in list(line):
            if char in bracket_map:
                stack.append(char)
            else:
                if char == bracket_map[stack[-1]]:
                    stack.pop()
                else:
                    syntax_score += corrupted_score_map[char]
                    break
    return syntax_score


def part_2(file_path: str) -> int:
    with open(file_path, "r") as f:
        lines = f.read().splitlines()

    scores: list[int] = []

    for line in lines:
        stack = []
        corrupted = False
        for char in list(line):
            if char in bracket_map:
                stack.append(char)
            else:
                if char == bracket_map[stack[-1]]:
                    stack.pop()
                else:
                    corrupted = True
                    break
        if corrupted:
            continue
        score = 0
        while stack:
            score *= 5
            score += incomplete_score_map[bracket_map[stack.pop()]]
        scores.append(score)

    return int(statistics.median(scores))
