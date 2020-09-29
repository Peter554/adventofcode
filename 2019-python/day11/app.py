import os
import asyncio
import matplotlib.pyplot as plt

from intcode import IntCode


class Robot:
    def __init__(self, raw_data):
        self.input_queue = asyncio.Queue()
        self.computer = IntCode(raw_data, self.input_queue)
        self.painted = {}

    async def run(self, start_color=0):
        self._current_position = (0, 0)
        self._current_direction = 0
        self.painted = {(0, 0): [start_color]}

        async def cycle():
            while not self.computer.done:
                inpt = self._get_next_input()
                await self.input_queue.put(inpt)
                color = await self.computer.output_queue.get()
                turn = await self.computer.output_queue.get()
                self._paint(color)
                self._apply_turn(turn)

        await asyncio.gather(self.computer.run(), cycle())

    def _get_next_input(self):
        if self._current_position in self.painted:
            return self.painted[self._current_position][-1]
        else:
            return 0

    def _paint(self, color):
        if not (color in [0, 1]):
            raise Exception(f"Could not paint color {color}")
        if self._current_position in self.painted:
            self.painted[self._current_position].append(color)
        else:
            self.painted[self._current_position] = [color]

    def _apply_turn(self, turn):
        if turn == 0:
            next_direction = (self._current_direction - 1 + 4) % 4
        elif turn == 1:
            next_direction = (self._current_direction + 1) % 4
        else:
            raise Exception(f"Turn type {turn} not supported")
        if next_direction == 0:
            dx, dy = 0, 1
        elif next_direction == 1:
            dx, dy = 1, 0
        elif next_direction == 2:
            dx, dy = 0, -1
        elif next_direction == 3:
            dx, dy = -1, 0
        else:
            raise Exception(f"Could not handle next direction {next_direction}")
        next_position = (self._current_position[0] + dx, self._current_position[1] + dy)
        self._current_direction = next_direction
        self._current_position = next_position


def get_white_points(painted):
    white_points = [k for k, v in painted.items() if v[-1] == 1]
    return white_points


async def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(this_dir, "input.txt")

    with open(input_path) as f:
        raw_data = f.readline()
        robot = Robot(raw_data)
        print("Part 1")
        await robot.run()
        print(f"# panels painted at least once = {len(robot.painted.keys())}")
        print("Part 2")
        await robot.run(1)
        white_points = get_white_points(robot.painted)
        plt.scatter([v[0] for v in white_points], [v[1] for v in white_points])
        plt.show()
        # LRZECGFE


if __name__ == "__main__":
    asyncio.run(main())
