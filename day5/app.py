import os

from intcode import IntCode

if __name__ == "__main__":
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, 'input.txt')

    with open(input_path) as f:
        raw_code = f.readline()
        intcode = IntCode(raw_code)
        output = intcode.run(1)

        print('Part 1')
        print('Output = {}'.format(output))
