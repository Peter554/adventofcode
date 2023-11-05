from common.point2d import Point2D


def part_1(file_path: str) -> int:
    with open(file_path) as f:
        trees = {
            Point2D(idx_x, idx_y): int(char)
            for idx_y, line in enumerate(f.readlines())
            for idx_x, char in enumerate(line.strip())
        }

    visible_trees = set()
    for this_tree in trees:
        for delta in [Point2D(1, 0), Point2D(-1, 0), Point2D(0, 1), Point2D(0, -1)]:
            tree = this_tree
            while (next_tree := tree + delta) in trees and trees[next_tree] < trees[
                this_tree
            ]:
                tree = next_tree
            if next_tree not in trees:
                # we reached the edge of the forest 🎋
                visible_trees.add(this_tree)
                break
    return len(visible_trees)


def part_2(file_path: str) -> int:
    with open(file_path) as f:
        trees = {
            Point2D(idx_x, idx_y): int(char)
            for idx_y, line in enumerate(f.readlines())
            for idx_x, char in enumerate(line.strip())
        }

    treehouse_scores: dict[Point2D, int] = {}
    for this_tree in trees:
        treehouse_score = 1
        for delta in [Point2D(1, 0), Point2D(-1, 0), Point2D(0, 1), Point2D(0, -1)]:
            tree = this_tree
            direction_score = 0
            while (next_tree := tree + delta) in trees:
                direction_score += 1
                if trees[next_tree] >= trees[this_tree]:
                    break
                tree = next_tree
            treehouse_score *= direction_score
        treehouse_scores[this_tree] = treehouse_score
    return max(treehouse_scores.values())
