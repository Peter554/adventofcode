from day16.solution_part_1 import solve, get_valve_tour_flow, tweak_valve_tour


def test_get_valve_tour_flow():
    valves = {"BB": 13, "DD": 20}
    tunnel_paths = {"AA": {"BB": 1, "DD": 1}, "BB": {"DD": 2}, "DD": {"BB": 2}}

    valve_tour = ("DD", "BB")
    assert get_valve_tour_flow(valves, tunnel_paths, 1)(valve_tour) == 0
    assert get_valve_tour_flow(valves, tunnel_paths, 2)(valve_tour) == 0
    assert get_valve_tour_flow(valves, tunnel_paths, 3)(valve_tour) == 20
    assert get_valve_tour_flow(valves, tunnel_paths, 4)(valve_tour) == 20 * 2
    assert get_valve_tour_flow(valves, tunnel_paths, 5)(valve_tour) == 20 * 3
    assert get_valve_tour_flow(valves, tunnel_paths, 6)(valve_tour) == 20 * 4 + 13
    assert get_valve_tour_flow(valves, tunnel_paths, 7)(valve_tour) == 20 * 5 + 13 * 2
    assert get_valve_tour_flow(valves, tunnel_paths, 8)(valve_tour) == 20 * 6 + 13 * 3

    valve_tour = ("BB", "DD")
    assert get_valve_tour_flow(valves, tunnel_paths, 1)(valve_tour) == 0
    assert get_valve_tour_flow(valves, tunnel_paths, 2)(valve_tour) == 0
    assert get_valve_tour_flow(valves, tunnel_paths, 3)(valve_tour) == 13
    assert get_valve_tour_flow(valves, tunnel_paths, 4)(valve_tour) == 13 * 2
    assert get_valve_tour_flow(valves, tunnel_paths, 5)(valve_tour) == 13 * 3
    assert get_valve_tour_flow(valves, tunnel_paths, 6)(valve_tour) == 13 * 4 + 20
    assert get_valve_tour_flow(valves, tunnel_paths, 7)(valve_tour) == 13 * 5 + 20 * 2
    assert get_valve_tour_flow(valves, tunnel_paths, 8)(valve_tour) == 13 * 6 + 20 * 3


def test_tweak_valve_tour():
    valve_tour = ("A", "B", "C", "D", "E")
    tweaked_valve_tour = tweak_valve_tour(valve_tour)
    assert len(valve_tour) == len(tweaked_valve_tour)
    assert set(tweaked_valve_tour) == set(valve_tour)


def test_solve():
    assert solve("day16/sample") == 1651
    # assert solve("day16/input") == 1701
