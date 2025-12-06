import math
from pathlib import Path


def part_1(input: Path) -> int:
    problems = []
    for line in input.read_text().splitlines():
        for idx, word in enumerate(line.split()):
            if idx >= len(problems):
                problems.append([])
            if word.isnumeric():
                problems[idx].append(int(word))
            else:
                problems[idx].append(word)

    answers = []
    for problem in problems:
        match problem[-1]:
            case "+":
                answers.append(sum(problem[:-1]))
            case "*":
                answers.append(math.prod(problem[:-1]))
            case _:
                raise ValueError(f"Invalid operator: {problem[-1]}")

    return sum(answers)


def part_2(input: Path) -> int:
    text = [[c for c in line] for line in input.read_text().splitlines()]
    len_longest_line = max(len(line) for line in text)
    text = [line + [" "] * (len_longest_line - len(line)) for line in text]

    answers = []
    this_problem_numbers = []
    for col in range(len(text[0]) - 1, -1, -1):
        number: int | None = None
        operator: str | None = None
        for row in range(len(text)):
            char = text[row][col]
            if char.isnumeric():
                if number is None:
                    number = int(char)
                else:
                    number = 10 * number + int(char)
            elif char != " ":
                operator = char
        if number is not None:
            this_problem_numbers.append(number)
        if operator is not None:
            match operator:
                case "+":
                    answers.append(sum(this_problem_numbers))
                case "*":
                    answers.append(math.prod(this_problem_numbers))
                case _:
                    raise ValueError(f"Invalid operator: {operator}")
            this_problem_numbers = []

    return sum(answers)
