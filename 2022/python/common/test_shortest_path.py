import dataclasses

from common.shortest_path import find_shortest_paths, find_shortest_paths_simple

# https://de.wikipedia.org/wiki/Dijkstra-Algorithmus#Beispiel_mit_bekanntem_Zielknoten


@dataclasses.dataclass(frozen=True)
class City:
    name: str


FRANKFURT = City("FRANKFURT")
MANNHEIM = City("MANNHEIM")
KASSEL = City("KASSEL")
WUERZBURG = City("WUERZBURG")
KARLSRUHE = City("KARLSRUHE")
ERFURT = City("ERFURT")
NUERNBERG = City("NUERNBERG")
STUTTGART = City("STUTTGART")
AUGSBURG = City("AUGSBURG")
MUENCHEN = City("MUENCHEN")

CONNECTIONS = {
    FRANKFURT: (
        (85, MANNHEIM),
        (217, WUERZBURG),
        (173, KASSEL),
    ),
    MANNHEIM: (
        (85, FRANKFURT),
        (80, KARLSRUHE),
    ),
    KASSEL: (
        (173, FRANKFURT),
        (502, MUENCHEN),
    ),
    WUERZBURG: (
        (217, FRANKFURT),
        (186, ERFURT),
        (103, NUERNBERG),
    ),
    KARLSRUHE: (
        (80, MANNHEIM),
        (250, AUGSBURG),
    ),
    ERFURT: ((186, WUERZBURG),),
    NUERNBERG: (
        (103, WUERZBURG),
        (183, STUTTGART),
        (167, MUENCHEN),
    ),
    STUTTGART: ((183, NUERNBERG),),
    AUGSBURG: (
        (250, KARLSRUHE),
        (84, MUENCHEN),
    ),
    MUENCHEN: (
        (84, AUGSBURG),
        (167, NUERNBERG),
        (502, KASSEL),
    ),
}


def test_find_paths():
    shortest_paths = find_shortest_paths(FRANKFURT, lambda city: CONNECTIONS[city])
    shortest_path = shortest_paths[MUENCHEN]
    assert shortest_path.cost == 487
    assert shortest_path.states == (
        FRANKFURT,
        WUERZBURG,
        NUERNBERG,
        MUENCHEN,
    )
    assert shortest_path.origin == FRANKFURT
    assert shortest_path.destination == MUENCHEN

    assert (
        find_shortest_paths_simple(FRANKFURT, lambda city: CONNECTIONS[city])[MUENCHEN]
        == 487
    )
