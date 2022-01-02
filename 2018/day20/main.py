import argparse
import functools
import heapq

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("file_path")
args = arg_parser.parse_args()

with open(args.file_path) as f:
    pattern = f.read().strip()

# paths = set()
# to_check = [pattern]
# while to_check:
#     pattern = to_check.pop()
#     j = pattern.find(")")
#     if j < 0:
#         paths.add(pattern)
#     else:
#         i = pattern.rfind("(", 0, j)
#         for s in pattern[i + 1 : j].split("|"):
#             to_check.append(pattern[:i] + s + pattern[j + 1 :])
#
# room_min_distances = {}
# for path in paths:
#     room = (path.count("S") - path.count("N"), path.count("E") - path.count("W"))
#     distance = len(path)
#     if room not in room_min_distances or distance < room_min_distances[room]:
#         room_min_distances[room] = distance
#
# print(max(room_min_distances.values()))


rooms = {(0, 0)}
doors = set()


def draw(rooms, doors):
    i_min = min([i for i, _ in rooms])
    i_max = max([i for i, _ in rooms])
    j_min = min([j for _, j in rooms])
    j_max = max([j for _, j in rooms])
    s = ""
    for i in range(i_min, i_max + 1):
        for j in range(j_min, j_max + 1):
            if (i, j) in rooms:
                if (i, j) == (0, 0):
                    s += "X"
                else:
                    s += "."
            elif (i, j) in doors:
                s += "-" if (i - i_min) % 2 else "|"
            else:
                s += "#"
        s += "\n"
    print(s)


@functools.cache
def match_bracket(s, i):
    assert s[i] == "("
    count = 0
    pipes = []
    for j, char in enumerate(s[i:]):
        if char == "(":
            count += 1
        elif char == ")":
            count -= 1
            if count == 0:
                break
        elif char == "|" and count == 1:
            pipes.append(i + j)
    return i + j, tuple(pipes)


q = [(0, (0, 0), ())]
seen = set()
while q:
    q_item = q.pop()
    seen.add(q_item)
    idx, (i, j), goto = q_item
    while idx < len(pattern):
        char = pattern[idx]
        if char == "N":
            rooms.add((i - 2, j))
            doors.add((i - 1, j))
            i -= 2
            idx += 1
        elif char == "S":
            rooms.add((i + 2, j))
            doors.add((i + 1, j))
            i += 2
            idx += 1
        elif char == "W":
            rooms.add((i, j - 2))
            doors.add((i, j - 1))
            j -= 2
            idx += 1
        elif char == "E":
            rooms.add((i, j + 2))
            doors.add((i, j + 1))
            j += 2
            idx += 1
        elif char == "(":
            closing_idx, pipe_idxs = match_bracket(pattern, idx)
            for sub_idx in (idx, *pipe_idxs):
                q_item = (sub_idx + 1, (i, j), (*goto, closing_idx + 1))
                if q_item not in seen:
                    q.append(q_item)
            break
        elif char == "|" or char == ")":
            q_item = (goto[-1], (i, j), goto[:-1])
            if q_item not in seen:
                q.append(q_item)
            break

# print(pattern)
# draw(rooms, doors)


def neighbourhood(p):
    i, j = p
    return (
        ((i - 1, j), (i - 2, j)),
        ((i + 1, j), (i + 2, j)),
        ((i, j - 1), (i, j - 2)),
        ((i, j + 1), (i, j + 2)),
    )


min_distances = {(0, 0): 0}
q = []
heapq.heappush(q, (0, (0, 0)))
while q:
    _, p = heapq.heappop(q)
    for door, room in neighbourhood(p):
        if door in doors and room in rooms:
            distance = min_distances[p] + 1
            if room not in min_distances or distance < min_distances[room]:
                min_distances[room] = distance
                heapq.heappush(q, (distance, room))

print(max(min_distances.values()))
print(len({k for k, v in min_distances.items() if v >= 1000}))
