import os
import queue
import threading

from intcode import IntCode


def run_robot(raw_data):
    input_queue = queue.SimpleQueue()
    computer = IntCode(raw_data, input_queue)
    current_position = (0, 0)
    current_direction = 0
    painted = {}
    done = False

    def target():
        while not done:
            inpt = get_next_input(painted, current_position)
            input_queue.put(inpt)
            color = computer.output_queue.get()
            turn = computer.output_queue.get()
            paint(painted, current_position, color)
            current_position = \
                apply_turn(current_position, current_direction, turn)

    thread = threading.Thread(target=target)
    thread.start()

    _ = computer.run()
    done = True
    return painted


def get_next_input(painted, current_position):
    if not (current_position in painted):
        return 0
    return painted[current_position][-1]


def paint(painted, current_position, color):
    if not (current_position in painted):
        painted[current_position] = [color]
        return
    painted[current_position].append(color)


def apply_turn(current_position, current_direction, turn):
    if turn == 0:
        next_direction = (current_direction - 1 + 4) % 4
    elif turn == 1:
        next_direction = (current_direction + 1) % 4
    else:
        raise Exception(f'Turn type {turn} not supported')
    if next_direction == 0:
        dx, dy = 0, 1
    elif next_direction == 1:
        dx, dy = 1, 0
    elif next_direction == 2:
        dx, dy = 0, -1
    elif next_direction == 3:
        dx, dy = -1, 0
    else:
        raise Exception(f'Could not handle next direction {next_direction}')
    return (current_position[0] + dx, current_position[1] + dy)


if __name__ == '__main__':
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, 'input.txt')

    with open(input_path) as f:
        raw_code = f.readline()
        painted = run_robot(raw_code)
        print('Part 1')
        print(f'# panels painted at least once = {len(painted.keys())}')
        print('Part 2')
        print(f'')
