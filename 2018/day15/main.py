import argparse
import dataclasses
import heapq

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("file_path")
arg_parser.add_argument("elf_attack")
args = arg_parser.parse_args()

with open(args.file_path) as f:
    lines = f.read().splitlines()


@dataclasses.dataclass(eq=False)
class Warrior:
    attack: int
    health: int


env = set()
elves = {}
goblins = {}

for i, line in enumerate(lines):
    for j, char in enumerate(line):
        if char != "#":
            env.add((i, j))
        if char == "E":
            elves[(i, j)] = Warrior(attack=int(args.elf_attack), health=200)
        elif char == "G":
            goblins[(i, j)] = Warrior(attack=3, health=200)

n_elves_start = len(elves)


def draw(env, elves, goblins):
    i_min = min([i for i, _ in env])
    j_min = min([j for _, j in env])
    i_max = max([i for i, _ in env])
    j_max = max([j for _, j in env])
    s = ""
    for i in range(i_min, i_max + 1):
        for j in range(j_min, j_max + 1):
            if (i, j) in elves:
                s += "E"
            elif (i, j) in goblins:
                s += "G"
            elif (i, j) in env:
                s += "."
            else:
                s += "#"
        s += "\n"
    print(s)


def neighbourhood(p):
    i, j = p
    return (
        (i, j - 1),
        (i - 1, j),
        (i + 1, j),
        (i, j + 1),
    )


def min_distances(env, elves, goblins, p):
    assert p in env and p not in elves and p not in goblins
    md = {p: 0}
    q = []
    heapq.heappush(q, (0, p))
    while q:
        _, p = heapq.heappop(q)
        for np in neighbourhood(p):
            if np not in env or np in elves or np in goblins:
                continue
            d = md[p] + 1
            if np not in md or d < md[np]:
                md[np] = d
                heapq.heappush(q, (d, np))
    return md


done = False
round_number = 0
while not done:
    round_number += 1
    draw(env, elves, goblins)
    for p in sorted((*elves.keys(), *goblins.keys())):
        warrior = elves.get(p) or goblins.get(p)
        if warrior is None:
            # died during this round
            continue

        friends = elves if p in elves else goblins
        enemies = goblins if friends is elves else elves
        if not enemies:
            done = True
            break

        attackable_enemies = sorted(
            [
                (enemies[np].health, np, enemies[np])
                for np in neighbourhood(p)
                if np in enemies
            ]
        )
        if attackable_enemies:
            _, np, enemy_to_attack = attackable_enemies[0]
            enemy_to_attack.health -= warrior.attack
            if enemy_to_attack.health <= 0:
                del enemies[np]
            continue

        move_targets = []
        for ep in enemies:
            for enp in neighbourhood(ep):
                if enp not in env or enp in friends or enp in enemies:
                    continue
                md = min_distances(env, elves, goblins, enp)
                for np in neighbourhood(p):
                    if np in md:
                        move_targets.append((md[np], enp, np))

        if move_targets:
            del friends[p]
            move_targets = sorted(move_targets)
            _, _, p = move_targets[0]
            friends[p] = warrior
        else:
            continue

        attackable_enemies = sorted(
            [
                (enemies[np].health, np, enemies[np])
                for np in neighbourhood(p)
                if np in enemies
            ]
        )
        if attackable_enemies:
            _, np, enemy_to_attack = attackable_enemies[0]
            enemy_to_attack.health -= warrior.attack
            if enemy_to_attack.health <= 0:
                del enemies[np]


rounds_completed = round_number - 1
remaining_health = sum([w.health for w in {**elves, **goblins}.values()])
outcome = remaining_health * rounds_completed
print(remaining_health, rounds_completed, outcome)

if len(elves) < n_elves_start:
    print("elven lives were lost :(")
else:
    print("elves will never be defeated!")
