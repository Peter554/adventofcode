import argparse
import re

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("file_path")
args = arg_parser.parse_args()

clay = set()
falling_water = set()
static_water = set()

with open(args.file_path) as f:
    for line in f.read().splitlines():
        match = re.match(r"^(x|y)=(\d+), (x|y)=(\d+)..(\d+)", line)
        if match.group(1) == "x":
            assert match.group(3) == "y"
            j = int(match.group(2))
            for i in range(int(match.group(4)), int(match.group(5)) + 1):
                clay.add((i, j))
        elif match.group(1) == "y":
            assert match.group(3) == "x"
            i = int(match.group(2))
            for j in range(int(match.group(4)), int(match.group(5)) + 1):
                clay.add((i, j))


def draw(clay, falling_water, static_water):
    i_min = min([i for i, _ in clay])
    i_max = max([i for i, _ in clay])
    j_min = min([j for _, j in clay])
    j_max = max([j for _, j in clay])
    s = ""
    for i in range(i_min, i_max + 1):
        for j in range(j_min - 1, j_max + 2):
            assert sum([(i, j) in s for s in (clay, falling_water, static_water)]) <= 1
            if (i, j) in clay:
                s += "#"
            elif (i, j) in falling_water:
                s += "|"
            elif (i, j) in static_water:
                s += "~"
            else:
                s += "."
        s += "\n"
    print(s)


i_min = min([i for i, _ in clay])
i_max = max([i for i, _ in clay])

source_q = [(i_min, 500)]
sources_done = set()
while source_q:
    i, j = source_q.pop()
    if (i, j) in sources_done:
        continue
    j_center = j
    sources_done.add((i, j))

    while (i, j) not in clay and i <= i_max:
        falling_water.add((i, j))
        i += 1

    if i > i_max:
        continue

    sources = set()
    while not sources:
        i -= 1
        water_to_add = set()
        j = j_center
        while (i, j) not in clay and ((i + 1, j) in clay or (i + 1, j) in static_water):
            water_to_add.add((i, j))
            j += 1
        if (i, j) not in clay:
            sources.add((i, j))
        j = j_center
        while (i, j) not in clay and ((i + 1, j) in clay or (i + 1, j) in static_water):
            water_to_add.add((i, j))
            j -= 1
        if (i, j) not in clay:
            sources.add((i, j))
        if sources:
            falling_water.update(water_to_add)
        else:
            static_water.update(water_to_add)

    falling_water -= static_water
    source_q.extend(sources)


draw(clay, falling_water, static_water)
print("static water: ", len(static_water))
print("all water: ", len([*falling_water, *static_water]))
