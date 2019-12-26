import os
import random

from intcode import IntCode
from consoledrawer import ConsoleDrawer


if __name__ == "__main__":
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, 'input.txt')
    with open(input_path) as f:
        raw_code = f.readline()
        print(raw_code)
