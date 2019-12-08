import os
import re

if __name__ == "__main__":
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, "input.txt")

    with open(input_path) as f:
        raw_data = f.readline()
        layers = [raw_data[i:i+150] for i in range(0, len(raw_data), 150)]
        zeros_re = re.compile(r"0")
        ones_re = re.compile(r"1")
        twos_re = re.compile(r"2")
        zeros_per_layer = list(map(lambda x: len(zeros_re.findall(x)), layers))
        idx = zeros_per_layer.index(min(zeros_per_layer))
        ones = len(ones_re.findall(layers[idx]))
        twos = len(twos_re.findall(layers[idx]))
        print("Part 1")
        print(f"Answer = {ones * twos}")
