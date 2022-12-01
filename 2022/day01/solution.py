def part_1(file_path: str) -> int:
    with open(file_path) as f:
        calorie_groups = [
            [int(calorie) for calorie in calorie_group.splitlines()]
            for calorie_group in f.read().split("\n\n")
        ]
    return max(sum(calorie_group) for calorie_group in calorie_groups)


def part_2(file_path: str) -> int:
    with open(file_path) as f:
        calorie_groups = [
            [int(calorie) for calorie in calorie_group.splitlines()]
            for calorie_group in f.read().split("\n\n")
        ]
    return sum(sorted(sum(calorie_group) for calorie_group in calorie_groups)[-3:])
