def part_1(file_path: str) -> int:
    with open(file_path) as f:
        data = f.read()
    for i in range(len(data) - 4):
        block = data[i : i + 4]
        if len(set(block)) == 4:
            return i + 4
    assert False


def part_2(file_path: str) -> int:
    with open(file_path) as f:
        data = f.read()
    for i in range(len(data) - 14):
        block = data[i : i + 14]
        if len(set(block)) == 14:
            return i + 14
    assert False
