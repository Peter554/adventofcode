import os
import copy

from moon import Moon


def run_simulation(raw_data, n_steps):
    moons = [Moon(line) for line in raw_data]
    for i in range(n_steps):
        for moon in moons:
            moon.update_velocity(moons)
        for moon in moons:
            moon.update_position()
    return moons


if __name__ == '__main__':
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, 'input.txt')
    with open(input_path) as f:
        raw_data = f.readlines()
        print('Part 1')
        moons = run_simulation(raw_data, 1000)
        print(f'Total energy = {sum([m.energy() for m in moons])}')
        print('Part 2')
        print(f'')
