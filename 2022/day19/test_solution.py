from day19.solution import part_1, part_2, Blueprint, max_blueprint_geodes, Mineral


def test_max_blueprint_geodes():
    bp = Blueprint(
        1,
        {
            Mineral.ORE: {Mineral.ORE: 4},
            Mineral.CLAY: {Mineral.ORE: 2},
            Mineral.OBSIDIAN: {Mineral.ORE: 3, Mineral.CLAY: 14},
            Mineral.GEODE: {Mineral.ORE: 2, Mineral.OBSIDIAN: 7},
        },
    )
    assert max_blueprint_geodes(bp, 24) == 9


# def test_part_1():
#     assert part_1("day19/sample") == 33
#     assert part_1("day19/input") == 1958
#
#
# def test_part_2():
#     assert part_2("day19/input") == 4257
