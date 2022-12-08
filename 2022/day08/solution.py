from __future__ import annotations

import dataclasses


@dataclasses.dataclass(frozen=True)
class Point2D:
    x: int
    y: int

    def __add__(self, other: Point2D) -> Point2D:
        return Point2D(self.x + other.x, self.y + other.y)


def part_1(file_path: str) -> int:
    with open(file_path) as f:
        trees = {
            Point2D(idx_x, idx_y): int(char)
            for idx_y, line in enumerate(f.readlines())
            for idx_x, char in enumerate(line.strip())
        }
    max_idx_x, max_idx_y = max([dataclasses.astuple(tree) for tree in trees.keys()])

    directions = [
        # from left
        (
            [Point2D(0, idx_y) for idx_y in range(max_idx_y + 1)],
            Point2D(1, 0),
        ),
        # from right
        (
            [Point2D(max_idx_x, idx_y) for idx_y in range(max_idx_y + 1)],
            Point2D(-1, 0),
        ),
        # from top
        (
            [Point2D(idx_x, 0) for idx_x in range(max_idx_x + 1)],
            Point2D(0, 1),
        ),
        # from bottom
        (
            [Point2D(idx_x, max_idx_y) for idx_x in range(max_idx_x + 1)],
            Point2D(0, -1),
        ),
    ]

    trees_visible = set()
    for starting_trees, delta in directions:
        for starting_tree in starting_trees:
            tree = starting_tree
            trees_visible.add(tree)
            max_tree_height = trees[tree]
            while (next_tree := tree + delta) in trees:
                if trees[next_tree] > max_tree_height:
                    trees_visible.add(next_tree)
                    max_tree_height = trees[next_tree]
                tree = next_tree
    return len(trees_visible)


def part_2(file_path: str) -> int:
    with open(file_path) as f:
        trees = {
            Point2D(idx_x, idx_y): int(char)
            for idx_y, line in enumerate(f.readlines())
            for idx_x, char in enumerate(line.strip())
        }

    treehouse_scores: dict[Point2D, int] = {}
    for treehouse in trees:
        treehouse_height = trees[treehouse]
        treehouse_score = 1
        for delta in [Point2D(1, 0), Point2D(-1, 0), Point2D(0, 1), Point2D(0, -1)]:
            tree = treehouse
            treehouse_direction_score = 0
            while (next_tree := tree + delta) in trees:
                treehouse_direction_score += 1
                if trees[next_tree] >= treehouse_height:
                    break
                tree = next_tree
            treehouse_score *= treehouse_direction_score
        treehouse_scores[treehouse] = treehouse_score
    return max(treehouse_scores.values())
