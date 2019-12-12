import os

if __name__ == '__main__':
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, 'input.txt')
    with open(input_path) as f:
        raw_data = f.readlines()
        print('Part 1')
        print(f'')
        print('Part 2')
        print(f'')
