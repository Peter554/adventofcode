import os
import itertools
import queue
import threading

from intcode import IntCode


def run_permutation(permutation, raw_code):
    amp_a = IntCode(raw_code)
    amp_b = IntCode(raw_code, amp_a.output_queue)
    amp_c = IntCode(raw_code, amp_b.output_queue)
    amp_d = IntCode(raw_code, amp_c.output_queue)
    amp_e = IntCode(raw_code, amp_d.output_queue)
    amp_a.input_queue = queue.SimpleQueue()

    amp_a.input_queue.put(permutation[0])
    amp_a.input_queue.put(0)
    amp_b.input_queue.put(permutation[1])
    amp_c.input_queue.put(permutation[2])
    amp_d.input_queue.put(permutation[3])
    amp_e.input_queue.put(permutation[4])

    amp_a.run()
    amp_b.run()
    amp_c.run()
    amp_d.run()
    return amp_e.run()


def run_permutation_with_feedback(permutation, raw_code):
    amp_a = IntCode(raw_code)
    amp_b = IntCode(raw_code, amp_a.output_queue)
    amp_c = IntCode(raw_code, amp_b.output_queue)
    amp_d = IntCode(raw_code, amp_c.output_queue)
    amp_e = IntCode(raw_code, amp_d.output_queue)
    amp_a.input_queue = amp_e.output_queue

    amp_a.input_queue.put(permutation[0])
    amp_a.input_queue.put(0)
    amp_b.input_queue.put(permutation[1])
    amp_c.input_queue.put(permutation[2])
    amp_d.input_queue.put(permutation[3])
    amp_e.input_queue.put(permutation[4])

    def run_a():
        amp_a.run()

    thread_a = threading.Thread(target=run_a)
    thread_a.start()

    def run_b():
        amp_b.run()

    thread_b = threading.Thread(target=run_b)
    thread_b.start()

    def run_c():
        amp_c.run()

    thread_c = threading.Thread(target=run_c)
    thread_c.start()

    def run_d():
        amp_d.run()

    thread_d = threading.Thread(target=run_d)
    thread_d.start()

    return amp_e.run()


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
        print("Part 1")
        print("Max signal = {}".format(max_signal))

        max_signal = -1
        for permutation in itertools.permutations([5, 6, 7, 8, 9]):
            signal = run_permutation_with_feedback(permutation, raw_code)
            if signal > max_signal:
                max_signal = signal
        print("Part 2")
        print("Max signal = {}".format(max_signal))
