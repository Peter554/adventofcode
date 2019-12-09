import copy
import queue

from large_array import LargeArray


class IntCode():
    def __init__(self, raw_code, input_queue=None):
        self._original_code = \
            list(map(lambda x: int(x), raw_code.strip().split(',')))
        self.input_queue = input_queue
        self.output_queue = queue.SimpleQueue()

    def run(self):
        self._code = LargeArray(self._original_code)
        self._location = 0
        self._relative_base = 0
        self._last_output = None
        self._done = False

        while not self._done:
            self._step()

        return self._last_output

    def _step(self):
        op_code = self._code[self._location]
        op_type, parameter_modes = self._parse_op_code(op_code)

        if (op_type == 1):
            self._handle_add(parameter_modes)
        elif (op_type == 2):
            self._handle_mulitply(parameter_modes)
        elif (op_type == 3):
            self._handle_input(parameter_modes)
        elif (op_type == 4):
            self._handle_output(parameter_modes)
        elif (op_type == 5):
            self._handle_jump_if_true(parameter_modes)
        elif (op_type == 6):
            self._handle_jump_if_false(parameter_modes)
        elif (op_type == 7):
            self._handle_less_than(parameter_modes)
        elif (op_type == 8):
            self._handle_equal(parameter_modes)
        elif (op_type == 9):
            self._handle_adjust_relative_base(parameter_modes)
        elif (op_type == 99):
            self._done = True
        else:
            raise Exception(f'Operation {op_type} not supported')

    def _parse_op_code(self, op_code):
        op_type = op_code % 100
        parameter_modes = self._get_parameter_modes(op_code, 3)
        return op_type, parameter_modes

    def _get_parameter_modes(self, op_code, require_n):
        l = [int(x) for x in list(str(op_code)[:-2])]
        l.reverse()
        pad_n = require_n - len(l)
        l += [0] * pad_n
        return l

    def _get_parameter(self, offset, parameter_mode):
        value_at_offset = self._code[self._location + offset]
        if parameter_mode == 0:
            return self._code[value_at_offset]
        elif parameter_mode == 1:
            return value_at_offset
        elif parameter_mode == 2:
            return self._code[self._relative_base + value_at_offset]
        else:
            raise Exception(f'Parameter mode {parameter_mode} not supported')

    def _handle_add(self, parameter_modes):
        left = self._get_parameter(1, parameter_modes[0])
        right = self._get_parameter(2, parameter_modes[1])
        if parameter_modes[2] == 0:
            self._code[self._code[self._location + 3]] = left + right
        elif parameter_modes[2] == 2:
            self._code[self._relative_base +
                       self._code[self._location + 3]] = left + right
        else:
            msg = f'Add could not handle parameter mode {parameter_modes[2]}'
            raise Exception(msg)
        self._location += 4

    def _handle_mulitply(self, parameter_modes):
        left = self._get_parameter(1, parameter_modes[0])
        right = self._get_parameter(2, parameter_modes[1])
        if parameter_modes[2] == 0:
            self._code[self._code[self._location + 3]] = left * right
        elif parameter_modes[2] == 2:
            self._code[self._relative_base +
                       self._code[self._location + 3]] = left * right
        else:
            msg = f'Multiply could not handle parameter mode {parameter_modes[2]}'
            raise Exception(msg)
        self._location += 4

    def _handle_input(self, parameter_modes):
        inpt = self.input_queue.get()
        if parameter_modes[0] == 0:
            self._code[self._code[self._location + 1]] = inpt
        elif parameter_modes[0] == 2:
            self._code[self._relative_base +
                       self._code[self._location + 1]] = inpt
        else:
            msg = f'Input could not handle parameter mode {parameter_modes[0]}'
            raise Exception(msg)
        self._location += 2

    def _handle_output(self, parameter_modes):
        value = self._get_parameter(1, parameter_modes[0])
        self._last_output = value
        self.output_queue.put(value)
        self._location += 2

    def _handle_jump_if_true(self, parameter_modes):
        flag = self._get_parameter(1, parameter_modes[0])
        if flag != 0:
            self._location = self._get_parameter(2, parameter_modes[1])
        else:
            self._location += 3

    def _handle_jump_if_false(self, parameter_modes):
        flag = self._get_parameter(1, parameter_modes[0])
        if flag == 0:
            self._location = self._get_parameter(2, parameter_modes[1])
        else:
            self._location += 3

    def _handle_less_than(self, parameter_modes):
        left = self._get_parameter(1, parameter_modes[0])
        right = self._get_parameter(2, parameter_modes[1])
        value = 1 if left < right else 0
        if parameter_modes[2] == 0:
            self._code[self._code[self._location + 3]] = value
        elif parameter_modes[2] == 2:
            self._code[self._relative_base +
                       self._code[self._location + 3]] = value
        else:
            msg = f'Less than could not handle parameter mode {parameter_modes[2]}'
            raise Exception(msg)
        self._location += 4

    def _handle_equal(self, parameter_modes):
        left = self._get_parameter(1, parameter_modes[0])
        right = self._get_parameter(2, parameter_modes[1])
        value = 1 if left == right else 0
        if parameter_modes[2] == 0:
            self._code[self._code[self._location + 3]] = value
        elif parameter_modes[2] == 2:
            self._code[self._relative_base +
                       self._code[self._location + 3]] = value
        else:
            msg = f'Equal could not handle parameter mode {parameter_modes[2]}'
            raise Exception(msg)
        self._location += 4

    def _handle_adjust_relative_base(self, parameter_modes):
        self._relative_base += self._get_parameter(1, parameter_modes[0])
        self._location += 2