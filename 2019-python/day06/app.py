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
        orbits += 1
        active_node = active_node.parent
    return orbits


def count_tree_orbits(tree):
    orbits = 0
    orbits += count_node_orbits(tree)
    for child in tree.children:
        orbits += count_tree_orbits(child)
    return orbits


def find_node(tree, key):
    if tree.name == key:
        return tree

    for child in tree.children:
        found = find_node(child, key)
        if found is not None:
            return found

    return None


def get_parent_list(node):
    parents = []
    if node.parent is not None:
        parents.append(node.parent)
        parents.extend(get_parent_list(node.parent))
    return parents


if __name__ == "__main__":
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, 'input.txt')

    with open(input_path) as f:
        lines = f.readlines()
        lines = list(map(lambda line: line.strip(), lines))
        all_orbits = list(map(lambda line: (line[0:3], line[4:]), lines))

        tree = Node('COM', None)

        build_children(tree, all_orbits)

        print('Part 1')
        print('Total orbits = {}'.format(count_tree_orbits(tree)))

        santa = find_node(tree, 'SAN')
        me = find_node(tree, 'YOU')

        santas_parents = get_parent_list(santa)
        my_parents = get_parent_list(me)

        common = [node for node in santas_parents if node in my_parents]
        first_common = common[0]

        shortest_path_length = \
            santas_parents.index(first_common) + my_parents.index(first_common)

        print('Part 2')
        print('Shortest path length = {}'.format(shortest_path_length))
