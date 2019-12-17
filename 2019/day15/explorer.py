import itertools
import asyncio
import random

from intcode import IntCode


class Explorer():
    def __init__(self, raw_code):
        self._raw_code = raw_code

    async def explore(self):
        self._active_paths = set([()])
        self._paths = set()
        await self._discover_paths()
        return tuple(self._paths)

    async def _discover_paths(self):
        next_active_paths = set()
        for path in self._active_paths:
            candidates = Explorer.get_candidate_paths(path)
            results = []
            for candidate in candidates:
                result = await self._run_path(candidate)
                if result != 0:
                    next_active_paths.add(candidate)
                results.append(result)
            if all(r == 0 for r in results):
                self._paths.add(path)
        self._active_paths = next_active_paths
        if len(self._active_paths) > 0:
            await self._discover_paths()

    async def _run_path(self, path):
        computer = IntCode(self._raw_code, asyncio.Queue())
        task = asyncio.create_task(computer.run())
        for choice in path:
            await computer.input_queue.put(choice)
        out = -1
        for _ in path:
            out = await computer.output_queue.get()
        await computer.stop()
        await asyncio.gather(task)
        return out

    @staticmethod
    def get_candidate_paths(path):
        choices = [1, 2, 3, 4]
        if len(path) > 0:
            last = path[-1]
            if last == 1:
                choices.remove(2)
            elif last == 2:
                choices.remove(1)
            elif last == 3:
                choices.remove(4)
            elif last == 4:
                choices.remove(3)
        return tuple((*path, choice) for choice in choices)

    @staticmethod
    def apply_path(choices):
        path = [(0, 0)]
        for choice in choices:
            path.append(Explorer._update_position(path[-1], choice))
        return tuple(path)

    @staticmethod
    def _update_position(start, choice):
        if choice == 1:
            return (start[0] + 1, start[1])
        elif choice == 2:
            return (start[0] - 1, start[1])
        elif choice == 3:
            return (start[0], start[1] - 1)
        elif choice == 4:
            return (start[0], start[1] + 1)
        else:
            raise Exception(f'Choice {choice} not supported')
