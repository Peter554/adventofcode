from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class Node:
    value: int
    left: Node | None
    right: Node | None


def parse_nodes(lines: list[str], decryption_key: int) -> list[Node]:
    nodes = [Node(int(line) * decryption_key, None, None) for line in lines]
    nodes[0].left = nodes[-1]
    nodes[-1].right = nodes[0]
    for idx, l_node in enumerate(nodes[:-1]):
        r_node = nodes[idx + 1]
        l_node.right = r_node
        r_node.left = l_node
    return nodes


def normalize_node_value(value: int, n_nodes: int) -> int:
    return value % (n_nodes - 1)


def remove_node(node: Node):
    right = node.right
    left = node.left
    assert right is not None
    assert left is not None
    right.left = left
    left.right = right
    node.right = None
    node.left = None


def insert_node(node: Node, right: Node):
    left = right.left
    assert left is not None
    node.left = left
    node.right = right
    right.left = node
    left.right = node


def mix_nodes(nodes: list[Node]):
    for node in nodes:
        right = node.right
        remove_node(node)
        for _ in range(normalize_node_value(node.value, len(nodes))):
            assert right is not None
            right = right.right
        assert right is not None
        insert_node(node, right)


def part_1(file_path: str) -> int:
    with open(file_path) as f:
        nodes = parse_nodes(f.readlines(), 1)

    zero_nodes = [node for node in nodes if node.value == 0]
    assert len(zero_nodes) == 1
    zero_node = zero_nodes[0]

    mix_nodes(nodes)

    grove_coordinates: list[int] = []
    node = zero_node
    for i in range(1, 3001):
        assert node.right is not None
        node = node.right
        if i % 1000 == 0:
            grove_coordinates.append(node.value)
    return sum(grove_coordinates)


def part_2(file_path: str) -> int:
    with open(file_path) as f:
        nodes = parse_nodes(f.readlines(), 811589153)

    zero_nodes = [node for node in nodes if node.value == 0]
    assert len(zero_nodes) == 1
    zero_node = zero_nodes[0]

    for _ in range(10):
        mix_nodes(nodes)

    grove_coordinates: list[int] = []
    node = zero_node
    for i in range(1, 3001):
        assert node.right is not None
        node = node.right
        if i % 1000 == 0:
            grove_coordinates.append(node.value)
    return sum(grove_coordinates)
