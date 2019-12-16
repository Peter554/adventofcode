import os

from fft import Fft

if __name__ == "__main__":
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, 'input.txt')
    with open(input_path) as f:
        raw_code = f.readline()
        fft = Fft(raw_code)
        fft.advance_n(100)
        print('Part 1')
        print(f'{fft.get_state()}')
