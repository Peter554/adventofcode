import collections

from common.point3d import Point3D, Box3D

DELTAS_3D = (
    Point3D(1, 0, 0),
    Point3D(-1, 0, 0),
    Point3D(0, 1, 0),
    Point3D(0, -1, 0),
    Point3D(0, 0, 1),
    Point3D(0, 0, -1),
)


def part_1(file_path: str) -> int:
    with open(file_path) as f:
        lava: set[Point3D] = set()
        for line in f.readlines():
            x, y, z = line.strip().split(",")
            lava.add(Point3D(int(x), int(y), int(z)))

    lava_droplet_surface_area = 0
    for lava_cube in lava:
        for delta in DELTAS_3D:
            if lava_cube + delta not in lava:
                lava_droplet_surface_area += 1
    return lava_droplet_surface_area


def find_trapped_air(lava: set[Point3D], box: Box3D) -> set[Point3D]:
    exterior_air: set[Point3D] = set()
    q = collections.deque([box.bottom_left])
    while q:
        air = q.popleft()
        if air in exterior_air:
            continue
        exterior_air.add(air)
        q.extend(
            air + delta
            for delta in DELTAS_3D
            if box.contains(air + delta) and air + delta not in lava
        )
    return box.points - lava - exterior_air


def part_2(file_path: str) -> int:
    with open(file_path) as f:
        lava: set[Point3D] = set()
        for line in f.readlines():
            x, y, z = line.strip().split(",")
            lava.add(Point3D(int(x), int(y), int(z)))

    trapped_air = find_trapped_air(lava, Box3D(Point3D(0, 0, 0), Point3D(20, 20, 20)))

    lava_droplet_surface_area = 0
    for lava_cube in lava:
        for delta in DELTAS_3D:
            if lava_cube + delta not in lava and lava_cube + delta not in trapped_air:
                lava_droplet_surface_area += 1
    return lava_droplet_surface_area
