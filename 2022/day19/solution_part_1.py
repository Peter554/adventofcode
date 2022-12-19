import collections
import dataclasses
import enum
import re


class Mineral(enum.Enum):
    ORE = enum.auto()
    CLAY = enum.auto()
    OBSIDIAN = enum.auto()
    GEODE = enum.auto()


@dataclasses.dataclass(frozen=True)
class Blueprint:
    id: int
    robot_costs: dict[Mineral, dict[Mineral, int]]

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
        robot_costs: dict[Mineral, dict[Mineral, int]] = collections.defaultdict(dict)
        robot_costs[Mineral.ORE] = {Mineral.ORE: int(match.group(2))}
        robot_costs[Mineral.CLAY] = {Mineral.ORE: int(match.group(3))}
        robot_costs[Mineral.OBSIDIAN] = {
            Mineral.ORE: int(match.group(4)),
            Mineral.CLAY: int(match.group(5)),
        }
        robot_costs[Mineral.GEODE] = {
            Mineral.ORE: int(match.group(6)),
            Mineral.OBSIDIAN: int(match.group(7)),
        }
        return cls(int(match.group(1)), robot_costs)


def max_blueprint_geodes(bp: Blueprint) -> int:


def solve(file_path: str) -> int:
    with open(file_path) as f:
        blueprints = [Blueprint.parse(line.strip()) for line in f.readlines()]
    return sum(bp.id * max_blueprint_geodes(bp) for bp in blueprints)
