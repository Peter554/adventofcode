import collections


def part_1(file_path: str) -> int:
    with open(file_path, "r") as f:
        lines = f.read().splitlines()

    caves = collections.defaultdict(set)
    small_caves = set()
    for line in lines:
        cave_from, cave_to = line.split("-")
        caves[cave_from].add(cave_to)
        caves[cave_to].add(cave_from)
        for cave in (cave_from, cave_to):
            if cave == cave.lower():
                small_caves.add(cave)

    paths: set[tuple[str, ...]] = {("start",)}
    while True:
        for path in [*paths]:
            if path[-1] == "end":
                continue
            paths.remove(path)
            unvisitable = {cave for cave in path if cave in small_caves}
            for cave in caves[path[-1]] - unvisitable:
                paths.add((*path, cave))
        if all([p[-1] == "end" for p in paths]):
            break

    return len(paths)


def part_2(file_path: str) -> int:
    with open(file_path, "r") as f:
        lines = f.read().splitlines()

    caves = collections.defaultdict(set)
    small_caves = set()
    for line in lines:
        cave_from, cave_to = line.split("-")
        caves[cave_from].add(cave_to)
        caves[cave_to].add(cave_from)
        for cave in (cave_from, cave_to):
            if cave == cave.lower():
                small_caves.add(cave)

    paths: set[tuple[str, ...]] = {("start",)}
    while True:
        for path in [*paths]:
            if path[-1] == "end":
                continue
            paths.remove(path)
            small_cave_visits = collections.Counter(
                [cave for cave in path if cave in small_caves]
            )
            if 2 in small_cave_visits.values():
                unvisitable = {cave for cave in path if cave in small_caves}
            else:
                unvisitable = {"start"}
            for cave in caves[path[-1]] - unvisitable:
                paths.add((*path, cave))
        if all([p[-1] == "end" for p in paths]):
            break

    return len(paths)
