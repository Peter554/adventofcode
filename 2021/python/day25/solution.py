def part_1(file_path: str) -> int:
    with open(file_path, "r") as f:
        lines = f.read().splitlines()

    east_cucumbers = set()
    south_cucumbers = set()
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == ">":
                east_cucumbers.add((i, j))
            elif char == "v":
                south_cucumbers.add((i, j))

    i_size = i + 1
    j_size = j + 1

    step = 0
    while True:
        step += 1
        cucumbers_stationary = True

        all_cucumbers = east_cucumbers.union(south_cucumbers)

        next_east_cucumbers = set()
        for i, j in east_cucumbers:
            if (i, (j + 1) % j_size) in all_cucumbers:
                next_east_cucumbers.add((i, j))
            else:
                next_east_cucumbers.add((i, (j + 1) % j_size))
                cucumbers_stationary = False
        east_cucumbers = next_east_cucumbers

        all_cucumbers = east_cucumbers.union(south_cucumbers)

        next_south_cucumbers = set()
        for i, j in south_cucumbers:
            if ((i + 1) % i_size, j) in all_cucumbers:
                next_south_cucumbers.add((i, j))
            else:
                next_south_cucumbers.add(((i + 1) % i_size, j))
                cucumbers_stationary = False
        south_cucumbers = next_south_cucumbers

        if cucumbers_stationary:
            return step
