import os
import copy


def add_values(lst, idx_x, idx_y, idx_insert):
    lst[idx_insert] = lst[idx_x] + lst[idx_y]


def multiply_values(lst, idx_x, idx_y, idx_insert):
    lst[idx_insert] = lst[idx_x] * lst[idx_y]


def run(code, noun, verb):
    code = copy.deepcopy(code)
    code[1] = noun
    code[2] = verb

    idx = 0

    while (True):
        operator = code[idx]

        if (operator == 1):
            add_values(code, code[idx + 1], code[idx + 2], code[idx + 3])
        elif (operator == 2):
            multiply_values(code, code[idx + 1],
                            code[idx + 2], code[idx + 3])
        elif (operator == 99):
            break
        else:
            raise Exception('Operator {} not supported'.format(operator))

        idx += 4

    return code[0]


def compute_noun_and_verb(code, required_output):
    for noun in range(100):
        for verb in range(100):
            output = run(code, noun, verb)

            if (output == required_output):
                return (noun, verb)


if __name__ == "__main__":
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, 'input.txt')

    with open(input_path) as f:
        line = f.readline()
        code = list(map(lambda x: int(x), line.strip().split(',')))

        print('Part 1')
        print('Output = {}'.format(run(code, 12, 2)))

        noun, verb = compute_noun_and_verb(code, 19690720)

        print('Part 2')
        print('Noun = {}, Verb = {}'.format(noun, verb))
