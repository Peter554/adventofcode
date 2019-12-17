import itertools
import asyncio
import random
import pickle
import os

from intcode import IntCode


class Explorer():
    def __init__(self, raw_code):
        self._raw_code = raw_code
        this_dir = os.path.dirname(os.path.abspath(__file__))
        self._results_path = os.path.join(this_dir, 'explorer-results.pickle')

    async def explore(self):
        if os.path.exists(self._results_path):
            with open(self._results_path, 'rb') as f:
                return pickle.load(f)

        self._active_paths = set([()])
        self._paths = set()
        self._oxygen = None
        self._walls = set()
        await self._discover_paths()

        built_paths = tuple(map(lambda x: Explorer._apply_path(x),
                                tuple(self._paths)))

        results = (built_paths, self._oxygen, tuple(self._walls))

        with open(self._results_path, 'wb') as f:
            pickle.dump(results, f)

        return results

    async def _discover_paths(self):
        next_active_paths = set()
        for path in self._active_paths:
            candidates = Explorer._get_candidate_paths(path)
            results = []
            for candidate in candidates:
                result = await self._run_path(candidate)
                if result != 0:
                    next_active_paths.add(candidate)
                if result == 0:
                    self._walls.add(Explorer._apply_path(candidate)[-1])
                if result == 2 and self._oxygen is None:
                    self._oxygen = Explorer._apply_path(candidate)[-1]
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
    def _get_candidate_paths(path):
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
    def _apply_path(choices):
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
