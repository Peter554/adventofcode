def simulate_fish(file_path: str, n_days: int) -> int:
    fish = [0] * 9
    with open(file_path, "r") as f:
        for n in f.readline().split(","):
            fish[int(n)] += 1

    for _ in range(n_days):
        t = fish[0]
        for i in range(8):
            fish[i] = fish[i + 1]
        fish[6] += t
        fish[8] = t

    return sum(fish)


def part_1(file_path: str) -> int:
    return simulate_fish(file_path, 80)


def part_2(file_path: str) -> int:
    return simulate_fish(file_path, 256)
