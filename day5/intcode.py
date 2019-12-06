import copy


class IntCode():
    def __init__(self, raw_code):
        self._original_code = \
            list(map(lambda x: int(x), raw_code.strip().split(',')))

    def run(self, input: int):
        self._code = copy.deepcopy(self._original_code)
        self._location = 0
        self._input = input
        self._output = []
        self._running = True

        while self._running:
            self._step()

        return self._output

    def _step(self):
        op = self._code[self._location]
        op_type = op % 100
        parameter_modes = self._get_parameter_modes(op)

        if (op_type == 1):
            self._handle_add(parameter_modes)
        elif (op_type == 2):
            self._handle_mulitply(parameter_modes)
        elif (op_type == 3):
            self._handle_input()
        elif (op_type == 4):
            self._handle_output(parameter_modes)
        elif (op_type == 99):
            self._running = False
        else:
            msg = 'Operation of type {} not supported'.format(op_type)
            raise Exception(msg)

    def _get_parameter_modes(self, op):
        l = list(map(lambda x: int(x), list(str(op)[:-2])))
        l.reverse()
        l.extend([0, 0, 0])
        return l

    def _handle_add(self, parameter_modes):
        left = self._code[self._location + 1] if parameter_modes[0] == 1 \
            else self._code[self._code[self._location + 1]]

        right = self._code[self._location + 2] if parameter_modes[1] == 1 \
            else self._code[self._code[self._location + 2]]

        self._code[self._code[self._location + 3]] = left + right
        self._location += 4

    def _handle_mulitply(self, parameter_modes):
        left = self._code[self._location + 1] if parameter_modes[0] == 1 \
            else self._code[self._code[self._location + 1]]

        right = self._code[self._location + 2] if parameter_modes[1] == 1 \
            else self._code[self._code[self._location + 2]]

        self._code[self._code[self._location + 3]] = left * right
        self._location += 4

    def _handle_input(self):
        self._code[self._code[self._location + 1]] = self._input
        self._location += 2

    def _handle_output(self, parameter_modes):
        value = self._code[self._location + 1] if parameter_modes[0] == 1 \
            else self._code[self._code[self._location + 1]]

        self._output.append(value)
        self._location += 2
