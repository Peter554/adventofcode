def part_1(x1: int, x2: int, y1: int, y2: int) -> int:
    assert x1 > 0 and y1 < 0 and x1 < x2 and y1 < y2

    def check_path(vx: int, vy: int) -> tuple[bool, int]:
        x, y = 0, 0
        y_max = 0
        while True:
            x += vx
            y += vy
            vx = vx - 1 if vx > 0 else 0
            vy -= 1
            y_max = y if y > y_max else y_max
            if x1 <= x <= x2 and y1 <= y <= y2:
                assert vy <= 0
                return True, y_max
            if x > x2 or y < y1:
                return False, y_max

    y_max = 0
    bound = x2 + 1  # a guess...
    for vx in range(1, bound):
        for vy in range(-bound, bound):
            ok, y_max_path = check_path(vx, vy)
            if ok and y_max_path > y_max:
                y_max = y_max_path
    return y_max


def part_2(x1: int, x2: int, y1: int, y2: int) -> int:
    assert x1 > 0 and y1 < 0 and x1 < x2 and y1 < y2

    def check_path(vx: int, vy: int) -> bool:
        x, y = 0, 0
        while True:
            x += vx
            y += vy
            vx = vx - 1 if vx > 0 else 0
            vy -= 1
            if x1 <= x <= x2 and y1 <= y <= y2:
                assert vy <= 0
                return True
            if x > x2 or y < y1:
                return False

    count = 0
    bound = x2 + 1  # a guess...
    for vx in range(1, bound):
        for vy in range(-bound, bound):
            ok = check_path(vx, vy)
            if ok:
                count += 1
    return count
