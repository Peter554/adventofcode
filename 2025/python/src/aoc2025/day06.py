import itertools
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
    text = transpose_text(input.read_text())

    answers = []
    this_problem_numbers = []
    for line in reversed(text.splitlines()):
        if not line:
            continue
        if line.endswith("+") or line.endswith("*"):
            this_problem_numbers.append(int(line[:-1]))
            match line[-1]:
                case "+":
                    answers.append(sum(this_problem_numbers))
                case "*":
                    answers.append(math.prod(this_problem_numbers))
                case _:
                    raise ValueError(f"Invalid operator: {line[-1]}")
            this_problem_numbers = []
        else:
            this_problem_numbers.append(int(line))

    return sum(answers)


def transpose_text(s: str) -> str:
    lines = s.splitlines()
    transposed_lines = [
        "".join(chars).rstrip()
        for chars in itertools.zip_longest(*lines, fillvalue=" ")
    ]
    return "\n".join(transposed_lines)
