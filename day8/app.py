import os
import re
import functools


def build_layers(raw_data, width, height):
    size = width * height
    layers = [raw_data[i:i+size] for i in range(0, len(raw_data), size)]
    return [[int(x) for x in layer] for layer in layers]


def apply_layer(img, layer):
    if img is None:
        img = [2] * len(layer)
    for idx in range(len(img)):
        if img[idx] == 2:
            img[idx] = layer[idx]
    return img


def decode(raw_data, width, height):
    layers = build_layers(raw_data, width, height)
    img = functools.reduce(apply_layer, layers)
    return [img[i:i+width] for i in range(0, len(img), width)]


if __name__ == "__main__":
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, "input.txt")

    with open(input_path) as f:
        raw_data = f.readline()
        layers = build_layers(raw_data, 26, 6)

        def count_zeros(layer):
            return len([x for x in layer if x == 0])
        zeros_per_layer = [count_zeros(layer) for layer in layers]
        idx = zeros_per_layer.index(min(zeros_per_layer))
        ones = len([x for x in layers[idx] if x == 1])
        twos = len([x for x in layers[idx] if x == 2])

        print("Part 1")
        print(f"Answer = {ones * twos}")

        img = decode(raw_data, 25, 6)

        print("Part 2")
        for row in img:
            print(row)
