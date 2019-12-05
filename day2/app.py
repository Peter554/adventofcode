import os


this_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(this_dir, 'input.txt')


def add_values(lst, idx_x, idx_y, idx_insert):
    lst[idx_insert] = lst[idx_x] + lst[idx_y]


def multiply_values(lst, idx_x, idx_y, idx_insert):
    lst[idx_insert] = lst[idx_x] * lst[idx_y]


def run(noun, verb):
    with open(input_path) as f:
        line = f.readline()
        code = list(map(lambda x: int(x), line.strip().split(',')))
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


print('Part 1')
print('Output = {}'.format(run(12, 2)))

done = False

for noun in range(100):
    for verb in range(100):
        out = run(noun, verb)

        if (out == 19690720):
            done = True
            break

    if done:
        break

print('Part 2')
print('Noun = {}, Verb = {}'.format(noun, verb))
