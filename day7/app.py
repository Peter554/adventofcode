import os
import itertools

from intcode import IntCode


def run_permutation(permutation, raw_code):
    amp_a = IntCode(raw_code)
    amp_b = IntCode(raw_code)
    amp_c = IntCode(raw_code)
    amp_d = IntCode(raw_code)
    amp_e = IntCode(raw_code)

    signal = amp_a.run([permutation[0], 0])[-1]
    signal = amp_b.run([permutation[1], signal])[-1]
    signal = amp_c.run([permutation[2], signal])[-1]
    signal = amp_d.run([permutation[3], signal])[-1]
    signal = amp_e.run([permutation[4], signal])[-1]

    return signal


if __name__ == "__main__":
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, "input.txt")
    with open(input_path) as f:
        raw_code = f.readline()
        max_signal = -1
        for permutation in itertools.permutations([0, 1, 2, 3, 4]):
            signal = run_permutation(permutation, raw_code)
            if signal > max_signal:
                max_signal = signal
        print('Part 1')
        print('Max signal = {}'.format(max_signal))
