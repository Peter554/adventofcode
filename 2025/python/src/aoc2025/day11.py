import dataclasses
import functools
import pathlib
from collections import deque

from frozendict import frozendict


def part_1(input: pathlib.Path) -> int:
    graph = parse_graph(input)

    @dataclasses.dataclass(frozen=True)
    class Path:
        devices: tuple[str, ...]

        def contains_cycle(self) -> bool:
            edges = set()
            for d1, d2 in zip(self.devices, self.devices[1:]):
                if (d1, d2) in edges:
                    return True
                edges.add((d1, d2))
            return False

    def count_paths(
        graph: frozendict[str, frozenset[str]],
        from_device: str,
        to_device: str,
    ) -> int:
        count_paths = 0
        q = deque([Path((from_device,))])
        while q:
            path = q.popleft()
            if path.devices[-1] == to_device:
                count_paths += 1
                continue
            for device in graph[path.devices[-1]]:  # type: ignore[invalid-argument-type]
                extended_path = Path((*path.devices, device))
                if extended_path.contains_cycle():
                    continue
                q.append(extended_path)

        return count_paths

    return count_paths(graph, "you", "out")


def part_2(input: pathlib.Path) -> int:
    graph = parse_graph(input)

    @functools.cache
    def count_paths(from_device: str, to_device: str) -> int:
        if from_device == to_device:
            return 1
        return sum(count_paths(device, to_device) for device in graph[from_device])  # type: ignore[invalid-argument-type]

    return (
        count_paths("svr", "fft")
        * count_paths("fft", "dac")
        * count_paths("dac", "out")
    ) + (
        count_paths("svr", "dac")
        * count_paths("dac", "fft")
        * count_paths("fft", "out")
    )


def parse_graph(input: pathlib.Path) -> frozendict[str, frozenset[str]]:
    graph = {}
    for line in input.read_text().splitlines():
        from_device = line.split(":")[0]
        to_devices = line.split(":")[1].strip().split()
        graph[from_device] = frozenset(to_devices)
        for to_device in to_devices:
            if to_device not in graph:
                graph[to_device] = frozenset()
    return frozendict(graph)


def export_graph(graph: frozendict[str, frozenset[str]]) -> None:
    # Export to CSV for Cosmograph
    with open("edges.csv", "w") as f:
        f.write("source,target\n")
        for node, neighbors in graph.items():
            for neighbor in neighbors:
                f.write(f"{node},{neighbor}\n")
