from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class Node:
    value: int
    left: Node | None
    right: Node | None


def parse_nodes(lines: list[str]) -> list[Node]:
    nodes = [Node(int(line), None, None) for line in lines]
    nodes[0].left = nodes[-1]
    nodes[-1].right = nodes[0]
    for idx, l_node in enumerate(nodes[:-1]):
        r_node = nodes[idx + 1]
        l_node.right = r_node
        r_node.left = l_node
    return nodes


def remove_node(node: Node):
    right = node.right
    left = node.left
    right.left = left
    left.right = right
    node.right = None
    node.left = None


def insert_node(node: Node, right: Node):
    left = right.left
    node.left = left
    node.right = right
    right.left = node
    left.right = node


def print_nodes(root: Node):
    nodes = [root]
    while nodes[-1].right not in nodes:
        nodes.append(nodes[-1].right)
    nodes.append(nodes[-1].right)
    s = " -> ".join([f"{node.value}" for node in nodes])
    print(s)


def part_1(file_path: str) -> int:
    with open(file_path) as f:
        nodes = parse_nodes(f.readlines())

    zero_nodes = [node for node in nodes if node.value == 0]
    assert len(zero_nodes) == 1
    zero_node = zero_nodes[0]

    for node in nodes:
        if node.value == 0:
            continue
        right = node.right
        remove_node(node)
        if node.value >= 0:
            for _ in range(node.value):
                right = right.right
        else:
            for _ in range(abs(node.value)):
                right = right.left
        insert_node(node, right)

    grove_coordinates: list[int] = []
    node = zero_node
    for i in range(1, 3001):
        node = node.right
        if i % 1000 == 0:
            grove_coordinates.append(node.value)
    return sum(grove_coordinates)


def part_2(file_path: str) -> int:
    return 1
