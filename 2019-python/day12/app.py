import os
import copy
import numpy as np

from moon import Moon
from moonsperiodcalculator import MoonsPeriodCalculator


def run_simulation(raw_data, n_steps):
    moons = [Moon(line) for line in raw_data]
    for i in range(n_steps):
        step(moons)
    return moons


def find_period(raw_data):
    moons = [Moon(line) for line in raw_data]
    x_calculator = MoonsPeriodCalculator(lambda m: f"{m.p.x}:{m.v.x}", moons)
    y_calculator = MoonsPeriodCalculator(lambda m: f"{m.p.y}:{m.v.y}", moons)
    z_calculator = MoonsPeriodCalculator(lambda m: f"{m.p.z}:{m.v.z}", moons)
    x_period = None
    y_period = None
    z_period = None
    while True:
        step(moons)
        x_period = x_calculator.next(moons)
        y_period = y_calculator.next(moons)
        z_period = z_calculator.next(moons)
        if (x_period is not None) and (y_period is not None) and (z_period is not None):
            break
    return np.lcm.reduce([x_period, y_period, z_period])


def step(moons):
    for moon in moons:
        moon.update_velocity(moons)
    for moon in moons:
        moon.update_position()


if __name__ == "__main__":
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, "input.txt")
    with open(input_path) as f:
        raw_data = f.readlines()
        print("Part 1")
        moons = run_simulation(raw_data, 1000)
        print(f"Total energy = {sum([m.energy() for m in moons])}")
        print("Part 2")
        period = find_period(raw_data)
        print(f"Period = {period}")
