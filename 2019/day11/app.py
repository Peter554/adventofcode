import os
import queue
import threading

from intcode import IntCode


class Robot():
    def __init__(self, raw_data):
        self.input_queue = queue.SimpleQueue()
        self.computer = IntCode(raw_data, self.input_queue)
        self.current_position = (0, 0)
        self.current_direction = 0
        self.painted = {(0, 0): [1]}
        self.computer_output = None

    def run(self):
        def target():
            while self.computer_output is None:
                inpt = self._get_next_input()
                self.input_queue.put(inpt)
                color = self.computer.output_queue.get()
                turn = self.computer.output_queue.get()
                self._paint(color)
                self._apply_turn(turn)

        thread = threading.Thread(target=target)
        thread.start()
        self.computer_output = self.computer.run()
        thread.join()

    def _get_next_input(self):
        if self.current_position in self.painted:
            return self.painted[self.current_position][-1]
        else:
            return 0

    def _paint(self, color):
        if not (color in [0, 1]):
            raise Exception(f'Could not paint color {color}')
        if self.current_position in self.painted:
            self.painted[self.current_position].append(color)
        else:
            self.painted[self.current_position] = [color]

    def _apply_turn(self, turn):
        if turn == 0:
            next_direction = (self.current_direction - 1 + 4) % 4
        elif turn == 1:
            next_direction = (self.current_direction + 1) % 4
        else:
            raise Exception(f'Turn type {turn} not supported')
        if next_direction == 0:
            dx, dy = 0, 1
        elif next_direction == 1:
            dx, dy = 1, 0
        elif next_direction == 2:
            dx, dy = 0, -1
        elif next_direction == 3:
            dx, dy = -1, 0
        else:
            raise Exception(
                f'Could not handle next direction {next_direction}')
        next_position = (
            self.current_position[0] + dx, self.current_position[1] + dy)
        self.current_direction = next_direction
        self.current_position = next_position


if __name__ == '__main__':
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, 'input.txt')

    with open(input_path) as f:
        raw_data = f.readline()
        robot = Robot(raw_data)
        robot.run()
        print('Part 1')
        print(f'# panels painted at least once = {len(robot.painted.keys())}')
        print('Part 2')
        print(f'')
