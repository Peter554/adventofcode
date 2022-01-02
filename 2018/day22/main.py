import itertools
import heapq

# sample
# depth = 510
# target = (10, 10)

# input
depth = 9171
target = (7, 721)

################################################################################

# (x,y) => (i,j)
target = (target[1], target[0])

geological_indexes = {}
erosion_levels = {}
cave_types = {}


def draw(cave_types, target):
    s = ""
    for i in range(target[0] + 1):
        for j in range(target[1] + 1):
            cave_type = cave_types[(i, j)]
            if cave_type == 0:
                s += "."
            elif cave_type == 1:
                s += "="
            elif cave_type == 2:
                s += "|"
        s += "\n"
    print(s)


f = 8
for (i, j) in itertools.product(range(f * target[0] + 1), range(f * target[1] + 1)):
    if (i, j) == (0, 0) or (i, j) == target:
        geological_indexes[(i, j)] = 0
    elif i == 0:
        geological_indexes[(i, j)] = 16807 * j
    elif j == 0:
        geological_indexes[(i, j)] = 48271 * i
    else:
        geological_indexes[(i, j)] = (
            erosion_levels[(i - 1, j)] * erosion_levels[(i, j - 1)]
        )
    erosion_levels[(i, j)] = (geological_indexes[(i, j)] + depth) % 20183
    cave_types[(i, j)] = erosion_levels[(i, j)] % 3

# cave types:
#   0: rocky
#   1: narrow
#   2: wet
# tools:
#   0: none
#   1: torch
#   2: climbing gear
#
# => cave compatible with tool iff cave_type != tool

min_distances = {(0, 0, 1): 0}
q = []
heapq.heappush(q, (0, (0, 0, 1)))
while q:
    _, (i, j, tool) = heapq.heappop(q)
    for np in (
        (i - 1, j),
        (i, j - 1),
        (i, j + 1),
        (i + 1, j),
    ):
        if np not in cave_types:
            continue
        if tool == cave_types[np]:
            continue
        distance = min_distances[(i, j, tool)] + 1
        if (*np, tool) not in min_distances or distance < min_distances[(*np, tool)]:
            min_distances[(*np, tool)] = distance
            heapq.heappush(q, (distance, (*np, tool)))
    for ntool in {0, 1, 2} - {tool, cave_types[(i, j)]}:
        distance = min_distances[(i, j, tool)] + 7
        if (i, j, ntool) not in min_distances or distance < min_distances[
            (i, j, ntool)
        ]:
            min_distances[(i, j, ntool)] = distance
            heapq.heappush(q, (distance, (i, j, ntool)))


print(min_distances[(*target, 1)])
