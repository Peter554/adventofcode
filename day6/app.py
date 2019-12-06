import os


class Node():
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.children = []

    def add_child(self, node):
        self.children.append(node)


def build_children(node, all_orbits):
    orbits = list(filter(lambda orbit: orbit[0] == node.name, all_orbits))
    if len(orbits) == 0:
        return
    for orbit in orbits:
        child = Node(orbit[1], node)
        node.add_child(child)
    for child in node.children:
        build_children(child, all_orbits)


def count_node_orbits(node):
    active_node = node
    orbits = 0
    while (active_node.parent is not None):
        orbits = orbits + 1
        active_node = active_node.parent
    return orbits


if __name__ == "__main__":
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, 'input.txt')

    with open(input_path) as f:
        lines = f.readlines()
        lines = list(map(lambda line: line.strip(), lines))
        all_orbits = list(map(lambda line: (line[0:3], line[4:]), lines))

        tree = Node('COM', None)

        build_children(tree, all_orbits)

        print(count_node_orbits(tree.children[0].children[0]))
