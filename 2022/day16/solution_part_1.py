from __future__ import annotations

import collections
import re

from common.shortest_path import find_shortest_paths_simple


Valves = dict[str, int]
TunnelConnections = dict[str, list[str]]
TunnelPaths = dict[str, dict[str, int]]
ValveTour: tuple[str, ...]


def parse_valves_and_tunnels(
    data: list[str],
) -> tuple[Valves, TunnelConnections]:
    valves: Valves = {}
    tunnels: TunnelConnections = collections.defaultdict(list)
    for line in data:
        match = re.match(
            r"^Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)$", line
        )
        assert match is not None
        valves[match.group(1)] = int(match.group(2))
        for tunnel in match.group(3).split(", "):
            tunnels[match.group(1)].append(tunnel)
    return valves, tunnels


def derive_tunnel_paths(tunnel_connections: TunnelConnections) -> TunnelPaths:
    tunnel_paths: TunnelPaths = collections.defaultdict(dict)
    for origin in tunnel_connections:
        shortest_paths = find_shortest_paths_simple(
            origin,
            lambda name: tuple(
                (1, destination) for destination in tunnel_connections[name]
            ),
        )
        for destination, cost in shortest_paths.items():
            tunnel_paths[origin][destination] = cost
    return tunnel_paths


def get_valve_tour_flow(valves: Valves, tunnel_paths: TunnelPaths, end_timestep: int):
    def f(vt: ValveTour) -> int:
        location = "AA"
        timestep = 0
        final_flow = 0
        for valve in vt:
            timestep += tunnel_paths[location][valve] + 1
            final_flow += max(end_timestep - timestep, 0) * valves[valve]
            location = valve
        return final_flow

    return f


def solve(file_path: str) -> int:
    with open(file_path) as f:
        data = [line.strip() for line in f.readlines()]
    valves, tunnel_connections = parse_valves_and_tunnels(data)
    tunnel_paths = derive_tunnel_paths(tunnel_connections)
    valves = {k: v for k, v in valves.items() if v != 0}

    return 1
