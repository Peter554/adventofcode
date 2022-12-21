from __future__ import annotations

import dataclasses
import re
import typing


class Expression(typing.Protocol):
    def evaluate(self, expression_lookup: dict[str, Expression]) -> float:
        ...


@dataclasses.dataclass(frozen=True)
class LiteralExpression:
    value: int

    def evaluate(self, expression_lookup: dict[str, Expression]) -> float:
        return self.value


@dataclasses.dataclass(frozen=True)
class AddExpression:
    left: str
    right: str

    def evaluate(self, expression_lookup: dict[str, Expression]) -> float:
        return expression_lookup[self.left].evaluate(
            expression_lookup
        ) + expression_lookup[self.right].evaluate(expression_lookup)


@dataclasses.dataclass(frozen=True)
class SubtractExpression:
    left: str
    right: str

    def evaluate(self, expression_lookup: dict[str, Expression]) -> float:
        return expression_lookup[self.left].evaluate(
            expression_lookup
        ) - expression_lookup[self.right].evaluate(expression_lookup)


@dataclasses.dataclass(frozen=True)
class MultiplyExpression:
    left: str
    right: str

    def evaluate(self, expression_lookup: dict[str, Expression]) -> float:
        return expression_lookup[self.left].evaluate(
            expression_lookup
        ) * expression_lookup[self.right].evaluate(expression_lookup)


@dataclasses.dataclass(frozen=True)
class DivideExpression:
    left: str
    right: str

    def evaluate(self, expression_lookup: dict[str, Expression]) -> float:
        return expression_lookup[self.left].evaluate(
            expression_lookup
        ) / expression_lookup[self.right].evaluate(expression_lookup)


def parse_expressions(lines: list[str]) -> dict[str, Expression]:
    expression_lookup: dict[str, Expression] = {}
    for line in lines:
        if (match := re.match(r"^(\w+): (\d+)$", line)) is not None:
            expression_lookup[match.group(1)] = LiteralExpression(int(match.group(2)))
        elif (match := re.match(r"^(\w+): (\w+) ([+\-*/]) (\w+)$", line)) is not None:
            expression_class = {
                "+": AddExpression,
                "-": SubtractExpression,
                "*": MultiplyExpression,
                "/": DivideExpression,
            }[match.group(3)]
            expression_lookup[match.group(1)] = expression_class(
                match.group(2), match.group(4)  # type:ignore
            )
        else:
            assert 0
    return expression_lookup


def part_1(file_path: str) -> float:
    with open(file_path) as f:
        expression_lookup = parse_expressions([line.strip() for line in f.readlines()])
    return expression_lookup["root"].evaluate(expression_lookup)


def find_zero(f: typing.Callable[[int], float], a: int, b: int) -> int:
    while True:
        c = (a + b) // 2
        if abs(f(c)) < 1e-9:
            return c
        elif f(a) * f(c) > 0:
            a = c
        else:
            b = c


def part_2(file_path: str) -> int:
    with open(file_path) as f:
        expression_lookup = parse_expressions([line.strip() for line in f.readlines()])

    root_expression = expression_lookup["root"]
    assert isinstance(root_expression, AddExpression)
    expression_lookup["root"] = SubtractExpression(
        root_expression.left, root_expression.right
    )

    def func(i: int) -> float:
        expression_lookup["humn"] = LiteralExpression(i)
        return expression_lookup["root"].evaluate(expression_lookup)

    return find_zero(func, 0, 10_000_000_000_000)
