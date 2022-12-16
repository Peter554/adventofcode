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
    return next_tunnel_paths, {k: v for k, v in valves.items() if v != 0 and k != "AA"}


class AgentState(typing.NamedTuple):
    location: str
    destination: str | None
    timesteps_to_destination: int | None


class TunnelState(typing.NamedTuple):
    timestep: int
    me: AgentState
    elephant: AgentState
    valves_closed: frozenset[str]
    flow_forecast: int


def get_next_tunnel_states(
    valves: Valves, tunnel_paths: TunnelPaths, max_timestep: int
):
    def f(ts: TunnelState) -> tuple[tuple[int, TunnelState], ...]:
        if ts.timestep == max_timestep:
            return ()
        elif not ts.valves_closed:
            return ()

        next_tunnel_states: list[tuple[int, TunnelState]] = []
        my_next_states = get_next_agent_states(
            ts.me, tunnel_paths, ts.timestep, max_timestep, ts.valves_closed
        )
        elephant_next_states = get_next_agent_states(
            ts.elephant, tunnel_paths, ts.timestep, max_timestep, ts.valves_closed
        )
        for my_next_state, my_valves_opening in my_next_states:
            for elephant_next_state, elephant_valves_opening in elephant_next_states:
                valves_opening = my_valves_opening.union(elephant_valves_opening)
                delta_flow_forecast = 0
                for valve_opening in valves_opening:
                    delta_flow_forecast += (max_timestep - ts.timestep - 1) * valves[
                        valve_opening
                    ]
                next_tunnel_state = TunnelState(
                    ts.timestep + 1,
                    my_next_state,
                    elephant_next_state,
                    frozenset(ts.valves_closed - valves_opening),
                    ts.flow_forecast + delta_flow_forecast,
                )
                next_tunnel_states.append((-delta_flow_forecast, next_tunnel_state))

        return tuple(next_tunnel_states)

    return f


def get_next_agent_states(
    agent: AgentState,
    tunnel_paths: TunnelPaths,
    timestep: int,
    max_timestep: int,
    valves_closed: frozenset[str],
) -> list[tuple[AgentState, set[str]]]:
    next_agent_states: list[tuple[AgentState, set[str]]] = []

    if agent.destination is None:
        for destination, destination_distance in tunnel_paths[agent.location].items():
            if destination not in valves_closed:
                continue  # no point going to an already open valve
            timesteps_to_turn_on_valve = destination_distance + 1
            if max_timestep - timestep - timesteps_to_turn_on_valve < 0:
                continue  # exceeded max_timestep
            next_agent_states.append(
                (
                    AgentState(
                        # timesteps_to_turn_on_valve - 1, since we already take one step this turn.
                        agent.location,
                        destination,
                        timesteps_to_turn_on_valve - 1,
                    ),
                    set(),
                )
            )
        if not next_agent_states:
            next_agent_states.append((agent, set()))
        return next_agent_states

    assert agent.timesteps_to_destination is not None
    if agent.timesteps_to_destination > 1:
        next_agent_states.append(
            (
                AgentState(
                    agent.location,
                    agent.destination,
                    agent.timesteps_to_destination - 1,
                ),
                set(),
            )
        )
        return next_agent_states

    valves_opening = {agent.destination}.intersection(valves_closed)
    next_agent_states.append(
        (AgentState(agent.destination, None, None), valves_opening)
    )
    return next_agent_states


def solve(file_path: str) -> int:
    with open(file_path) as f:
        data = [line.strip() for line in f.readlines()]
    valves, tunnels = parse_valves_and_tunnels(data)
    tunnel_paths = map_tunnel_paths(tunnels)
    tunnel_paths, valves = remove_useless_valves(tunnel_paths, valves)

    initial_tunnel_state = TunnelState(
        0,
        AgentState("AA", None, None),
        AgentState("AA", None, None),
        frozenset(valves),
        0,
    )
    paths = find_shortest_paths_simple(
        initial_tunnel_state,
        get_next_tunnel_states(valves, tunnel_paths, 26),
    )
    return max(destination.flow_forecast for destination in paths)
