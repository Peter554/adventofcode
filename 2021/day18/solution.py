from __future__ import annotations

import typing
import dataclasses
import math
import copy


@dataclasses.dataclass
class RegularNumber:
    parent: typing.Optional[SnailfishNumber]
    value: int

    def __str__(self) -> str:
        return str(self.value)

    @property
    def magnitude(self) -> int:
        return self.value

    def split(self) -> None:
        assert self.parent is not None
        parent = self.parent
        self.parent = None
        t = RegularNumber(None, 0)
        sfn = SnailfishNumber(parent, left=t, right=t)
        sfn.left = RegularNumber(sfn, value=math.floor(self.value / 2))
        sfn.right = RegularNumber(sfn, value=math.ceil(self.value / 2))
        if self is parent.left:
            parent.left = sfn
        elif self is parent.right:
            parent.right = sfn
        else:
            raise Exception("bad parent/child relation")


@dataclasses.dataclass
class SnailfishNumber:
    parent: typing.Optional[SnailfishNumber]
    left: typing.Union[RegularNumber, SnailfishNumber]
    right: typing.Union[RegularNumber, SnailfishNumber]

    def __str__(self) -> str:
        return f"[{str(self.left)},{str(self.right)}]"

    @classmethod
    def parse(cls, s: str) -> SnailfishNumber:
        snailfish_number = cls._parse(s, None)
        assert isinstance(snailfish_number, SnailfishNumber)
        return snailfish_number

    @classmethod
    def _parse(
        cls, s: str, parent: typing.Optional[SnailfishNumber]
    ) -> typing.Union[RegularNumber, SnailfishNumber]:
        if "," in s:
            s = s[1:-1]
            count = 0
            for idx, char in enumerate(s):
                if char == "[":
                    count += 1
                elif char == "]":
                    count -= 1
                elif char == "," and count == 0:
                    t = RegularNumber(None, 0)
                    snailfish_number = cls(
                        parent=parent,
                        left=t,
                        right=t,
                    )
                    left_str, right_str = s[:idx], s[idx + 1 :]
                    snailfish_number.left = cls._parse(left_str, snailfish_number)
                    snailfish_number.right = cls._parse(right_str, snailfish_number)
                    return snailfish_number
            raise Exception("failed to parse snail number")
        else:
            return RegularNumber(parent=parent, value=int(s))

    def __add__(self, other: SnailfishNumber) -> SnailfishNumber:
        assert self.parent is None and other.parent is None
        self = copy.deepcopy(self)  # copying is very slow :(
        other = copy.deepcopy(other)
        snailfish_number = SnailfishNumber(parent=None, left=self, right=other)
        self.parent = snailfish_number
        other.parent = snailfish_number
        while True:
            done = True
            for sfn in snailfish_number.left_to_right:
                if sfn.depth >= 4:
                    sfn.explode()
                    done = False
                    break
            if not done:
                continue
            for sfn in snailfish_number.left_to_right:
                if isinstance(sfn.left, RegularNumber) and sfn.left.value >= 10:
                    sfn.left.split()
                    done = False
                    break
                if isinstance(sfn.right, RegularNumber) and sfn.right.value >= 10:
                    sfn.right.split()
                    done = False
                    break
            if done:
                break
        return snailfish_number

    @property
    def left_to_right(self) -> tuple[SnailfishNumber, ...]:
        nodes: tuple[SnailfishNumber, ...] = ()
        if isinstance(self.left, SnailfishNumber):
            nodes = (*nodes, *self.left.left_to_right)
        nodes = (*nodes, self)
        if isinstance(self.right, SnailfishNumber):
            nodes = (*nodes, *self.right.left_to_right)
        return nodes

    @property
    def depth(self) -> int:
        if self.parent:
            return self.parent.depth + 1
        else:
            return 0

    @property
    def magnitude(self) -> int:
        return 3 * self.left.magnitude + 2 * self.right.magnitude

    def explode(self) -> None:
        assert self.parent is not None

        def handle_left() -> None:
            assert isinstance(self.left, RegularNumber)
            node: typing.Union[RegularNumber, SnailfishNumber] = self
            while True:
                if node.parent is None:
                    return
                if node.parent.left is node:
                    node = node.parent
                else:
                    node = node.parent.left  # type:ignore
                    break
            while isinstance(node, SnailfishNumber):
                node = node.right
            node.value += self.left.value

        def handle_right() -> None:
            assert isinstance(self.right, RegularNumber)
            node: typing.Union[RegularNumber, SnailfishNumber] = self
            while True:
                if node.parent is None:
                    return
                if node.parent.right is node:
                    node = node.parent
                else:
                    node = node.parent.right  # type:ignore
                    break
            while isinstance(node, SnailfishNumber):
                node = node.left
            node.value += self.right.value

        handle_left()
        handle_right()
        parent = self.parent
        self.parent = None
        if parent.left is self:
            parent.left = RegularNumber(parent, 0)
        elif parent.right is self:
            parent.right = RegularNumber(parent, 0)
        else:
            raise Exception("bad parent/child relation")


def part_1(file_path: str) -> int:
    with open(file_path, "r") as f:
        snailfish_numbers = [SnailfishNumber.parse(line.strip()) for line in f]
    snailfish_number = snailfish_numbers[0]
    for sfn in snailfish_numbers[1:]:
        snailfish_number = snailfish_number + sfn
    return snailfish_number.magnitude


def part_2(file_path: str) -> int:
    with open(file_path, "r") as f:
        snailfish_numbers = [SnailfishNumber.parse(line.strip()) for line in f]
    max_magnitude = 0
    for i, n in enumerate(snailfish_numbers):
        for j, m in enumerate(snailfish_numbers):
            if i == j:
                continue
            magnitude = (n + m).magnitude
            if magnitude > max_magnitude:
                max_magnitude = magnitude
    return max_magnitude
