from __future__ import annotations

import collections
import re
import typing

from common.shortest_path import find_shortest_paths_simple


Valves = dict[str, int]
Tunnels = dict[str, list[str]]
TunnelPaths = dict[str, dict[str, int]]


def parse_valves_and_tunnels(
    data: list[str],
) -> tuple[Valves, Tunnels]:
    valves: Valves = {}
    tunnels: Tunnels = collections.defaultdict(list)
    for line in data:
        match = re.match(
            r"^Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)$", line
        )
        assert match is not None
        valves[match.group(1)] = int(match.group(2))
        for tunnel in match.group(3).split(", "):
            tunnels[match.group(1)].append(tunnel)
    return valves, tunnels


def map_tunnel_paths(tunnels: Tunnels) -> TunnelPaths:
    tunnel_paths: TunnelPaths = collections.defaultdict(dict)
    for origin in tunnels:
        shortest_paths = find_shortest_paths_simple(
            origin,
            lambda name: tuple((1, destination) for destination in tunnels[name]),
        )
        for destination, cost in shortest_paths.items():
            tunnel_paths[origin][destination] = cost
    return tunnel_paths


def remove_useless_valves(
    tunnel_paths: TunnelPaths, valves: Valves
) -> tuple[TunnelPaths, Valves]:
    next_tunnel_paths: TunnelPaths = collections.defaultdict(dict)
    for origin, destinations in tunnel_paths.items():
        if valves[origin] == 0 and origin != "AA":
            continue
        for destination, cost in destinations.items():
            if valves[destination] == 0:
                continue
            next_tunnel_paths[origin][destination] = cost
    return next_tunnel_paths, {k: v for k, v in valves.items() if v != 0}


class TunnelState(typing.NamedTuple):
    timestep: int
    location: str
    valves_closed: frozenset[str]
    flow_forecast: int


def get_next_tunnel_states(
    valves: Valves, tunnel_paths: TunnelPaths, max_timestep: int
):
    def f(ts: TunnelState) -> tuple[tuple[int, TunnelState], ...]:
        next_tunnel_states: list[tuple[int, TunnelState]] = []
        for destination, destination_distance in tunnel_paths[ts.location].items():
            if destination not in ts.valves_closed:
                continue  # no point going to an already open valve
            timesteps_to_turn_on_valve = destination_distance + 1
            delta_flow_forecast = (
                max_timestep - ts.timestep - timesteps_to_turn_on_valve
            ) * valves[destination]
            if delta_flow_forecast < 0:
                continue  # exceeded max_timestep
            next_tunnel_state = TunnelState(
                ts.timestep + timesteps_to_turn_on_valve,
                destination,
                frozenset(ts.valves_closed - {destination}),
                ts.flow_forecast + delta_flow_forecast,
            )
            next_tunnel_states.append((-delta_flow_forecast, next_tunnel_state))
        return tuple(next_tunnel_states)

    return f


def solve(file_path: str) -> int:
    with open(file_path) as f:
        data = [line.strip() for line in f.readlines()]
    valves, tunnels = parse_valves_and_tunnels(data)
    tunnel_paths = map_tunnel_paths(tunnels)
    tunnel_paths, valves = remove_useless_valves(tunnel_paths, valves)

    initial_tunnel_state = TunnelState(0, "AA", frozenset(valves), 0)
    paths = find_shortest_paths_simple(
        initial_tunnel_state,
        get_next_tunnel_states(valves, tunnel_paths, 30),
    )
    return max(destination.flow_forecast for destination in paths)
