import os
import queue

from intcode import IntCode


def run_intcode(raw_code, inputs=[]):
    input_queue = queue.SimpleQueue()
    computer = IntCode(raw_code, input_queue)
    for value in inputs:
        input_queue.put(value)
    return computer.run()


if __name__ == '__main__':
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, 'input.txt')

    with open(input_path) as f:
        raw_code = f.readline()
        print('Part 1')
        print(f'Keycode = {run_intcode(raw_code, [1])}')
        print('Part 2')
