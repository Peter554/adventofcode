from __future__ import annotations

import collections
import dataclasses
import math
import re
import enum


class Mineral(enum.Enum):
    ORE = enum.auto()
    CLAY = enum.auto()
    OBSIDIAN = enum.auto()
    GEODE = enum.auto()

    def __repr__(self):
        return self.name


RobotCosts = dict[Mineral, dict[Mineral, int]]


@dataclasses.dataclass
class Blueprint:
    id: int
    robot_costs: RobotCosts

    @classmethod
    def parse(cls, s: str):
        match = re.match(
            r"^Blueprint (\d+): "
            r"Each ore robot costs (\d+) ore. "
            r"Each clay robot costs (\d+) ore. "
            r"Each obsidian robot costs (\d+) ore and (\d+) clay. "
            r"Each geode robot costs (\d+) ore and (\d+) obsidian.$",
            s,
        )
        assert match is not None
        robot_costs: RobotCosts = {}
        robot_costs[Mineral.ORE] = {
            Mineral.ORE: int(match.group(2)),
        }
        robot_costs[Mineral.CLAY] = {
            Mineral.ORE: int(match.group(3)),
        }
        robot_costs[Mineral.OBSIDIAN] = {
            Mineral.ORE: int(match.group(4)),
            Mineral.CLAY: int(match.group(5)),
        }
        robot_costs[Mineral.GEODE] = {
            Mineral.ORE: int(match.group(6)),
            Mineral.OBSIDIAN: int(match.group(7)),
        }
        return cls(int(match.group(1)), robot_costs)


@dataclasses.dataclass
class MiningState:
    timestep: int
    minerals: dict[Mineral, int]
    robots: dict[Mineral, int]


def should_build_robot(
    robot: Mineral,
    ms: MiningState,
    max_robot_cost: dict[Mineral, int],
    max_timestep: int,
) -> bool:
    if robot == Mineral.GEODE:
        return True
    if ms.robots[robot] >= max_robot_cost[robot]:
        return False
    if (
        ms.minerals[robot] + (max_timestep - ms.timestep) * ms.robots[robot]
        >= (max_timestep - ms.timestep) * max_robot_cost[robot]
    ):
        return False
    return True


def can_build_robot(robot: Mineral, ms: MiningState, bp: Blueprint) -> bool:
    for required_mineral, n in bp.robot_costs[robot].items():
        if ms.robots[required_mineral] == 0:
            return False
    return True


def build_robot(robot: Mineral, ms: MiningState, bp: Blueprint) -> MiningState:
    timesteps_to_build_robot = 0
    for required_mineral, n in bp.robot_costs[robot].items():
        timesteps_to_build_robot = max(
            timesteps_to_build_robot,
            math.ceil(
                max(n - ms.minerals[required_mineral], 0) / ms.robots[required_mineral]
            )
            + 1,
        )
    minerals = ms.minerals.copy()
    for mineral in Mineral:
        minerals[mineral] += timesteps_to_build_robot * ms.robots[
            mineral
        ] - bp.robot_costs[robot].get(mineral, 0)
    robots = ms.robots.copy()
    robots[robot] += 1
    return MiningState(
        ms.timestep + timesteps_to_build_robot,
        minerals,
        robots,
    )


def max_blueprint_geodes(bp: Blueprint, max_timestep: int) -> int:
    initial_robots: dict[Mineral, int] = collections.defaultdict(int)
    initial_robots[Mineral.ORE] += 1
    initial_state = MiningState(
        0,
        collections.defaultdict(int),
        initial_robots,
    )

    max_robot_cost: dict[Mineral, int] = {}
    max_robot_cost[Mineral.ORE] = max(
        robot_cost.get(Mineral.ORE, 0) for robot_cost in bp.robot_costs.values()
    )
    max_robot_cost[Mineral.CLAY] = max(
        robot_cost.get(Mineral.CLAY, 0) for robot_cost in bp.robot_costs.values()
    )
    max_robot_cost[Mineral.OBSIDIAN] = max(
        robot_cost.get(Mineral.OBSIDIAN, 0) for robot_cost in bp.robot_costs.values()
    )

    max_geodes = 0
    q = collections.deque([initial_state])
    while q:
        ms = q.popleft()
        if ms.minerals[Mineral.GEODE] > max_geodes:
            max_geodes = ms.minerals[Mineral.GEODE]

        next_states: list[MiningState] = []
        for next_robot_to_build in Mineral:
            if not should_build_robot(
                next_robot_to_build, ms, max_robot_cost, max_timestep
            ):
                continue
            if not can_build_robot(next_robot_to_build, ms, bp):
                continue
            next_state = build_robot(next_robot_to_build, ms, bp)
            if next_state.timestep <= max_timestep:
                next_states.append(next_state)

        if not next_states and ms.timestep < max_timestep:
            next_states.append(
                MiningState(
                    max_timestep,
                    {
                        mineral: ms.minerals[mineral]
                        + (max_timestep - ms.timestep) * ms.robots[mineral]
                        for mineral in Mineral
                    },
                    ms.robots,
                )
            )

        q.extend(next_states)

    return max_geodes


def part_1(file_path: str) -> int:
    with open(file_path) as f:
        blueprints = [Blueprint.parse(line.strip()) for line in f.readlines()]
    return sum(bp.id * max_blueprint_geodes(bp, 24) for bp in blueprints)


def part_2(file_path: str) -> int:
    with open(file_path) as f:
        blueprints = [Blueprint.parse(line.strip()) for line in f.readlines()]
    return (
        max_blueprint_geodes(blueprints[0], 32)
        * max_blueprint_geodes(blueprints[1], 32)
        * max_blueprint_geodes(blueprints[2], 32)
    )
