import os


def apply_command(lst, command):
    previous = lst[-1]

    direction = command[0]
    amount = int(command[1:])

    if direction == 'u':
        def action():
            lst.append((previous[0] + 1, previous[1]))
    elif direction == 'r':
        def action():
            lst.append((previous[0], previous[1] + 1))
    elif direction == 'd':
        def action():
            lst.append((previous[0] - 1, previous[1]))
    elif direction == 'l':
        def action():
            lst.append((previous[0], previous[1] - 1))
    else:
        raise Exception('Direction {} not supported'.format(direction))

    for _ in range(amount):
        action()


def build_wire_coordinates(text: str):
    commands = text.strip().lower().split(',')

    out = [(0, 0)]

    for command in commands:
        apply_command(out, command)

    out.pop(0)

    return out


if __name__ == "__main__":
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, 'input.txt')

    with open(input_path) as f:
        wire_1_raw = f.readline()
        wire_2_raw = f.readline()

        wire_1 = build_wire_coordinates(wire_1_raw)
        wire_2 = build_wire_coordinates(wire_2_raw)

        def in_wire_2(x):
            return any(map(lambda y: y[0] == x[0] and y[1] == x[1], wire_2))

        common = filter(in_wire_2, wire_1)

        print(list(common))
