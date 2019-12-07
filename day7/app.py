import os
import itertools

from intcode import IntCode


def run_permutation(permutation, raw_code):
    amp_a = IntCode(raw_code)
    amp_b = IntCode(raw_code)
    amp_c = IntCode(raw_code)
    amp_d = IntCode(raw_code)
    amp_e = IntCode(raw_code)

    signal, _ = amp_a.run([permutation[0], 0])
    signal, _ = amp_b.run([permutation[1], signal])
    signal, _ = amp_c.run([permutation[2], signal])
    signal, _ = amp_d.run([permutation[3], signal])
    signal, _ = amp_e.run([permutation[4], signal])

    return signal


def run_permutation_with_feedback(permutation, raw_code):
    amp_a = IntCode(raw_code)
    amp_b = IntCode(raw_code)
    amp_c = IntCode(raw_code)
    amp_d = IntCode(raw_code)
    amp_e = IntCode(raw_code)

    signal = None
    halted = False

    while not halted:
        signal, _ = amp_a.run(
            [permutation[0], 0 if signal is None else signal])

        signal, _ = amp_b.run([permutation[1], signal])
        signal, _ = amp_c.run([permutation[2], signal])
        signal, _ = amp_d.run([permutation[3], signal])
        signal, halted = amp_e.run([permutation[4], signal])

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

        max_signal = -1
        for permutation in itertools.permutations([5, 6, 7, 8, 9]):
            signal = run_permutation_with_feedback(permutation, raw_code)
            if signal > max_signal:
                max_signal = signal
        print('Part 2')
        print('Max signal = {}'.format(max_signal))
