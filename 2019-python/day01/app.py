import os
import math


def calculate_fuel_for_mass(mass):
    return math.floor(mass / 3) - 2


def calculate_fuel_for_mass_2(mass):
    fuel = math.floor(mass / 3) - 2

    if fuel > 0:
        return fuel + calculate_fuel_for_mass_2(fuel)

    return 0


if __name__ == "__main__":
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, "input.txt")

    with open(input_path) as f:
        total_fuel = 0

        for line in f:
            module_mass = float(line)
            module_fuel = calculate_fuel_for_mass(module_mass)
            total_fuel += module_fuel

        print("Part 1")
        print("Total fuel: {}".format(total_fuel))

        total_fuel = 0
        f.seek(0)

        for line in f:
            module_mass = float(line)
            module_fuel = calculate_fuel_for_mass_2(module_mass)
            total_fuel += module_fuel

        print("Part 2")
        print("Total fuel: {}".format(total_fuel))
