import pytest

from explorer import Explorer


@pytest.mark.parametrize(
    "paths,expect",
    [
        ((), ((1,), (2,), (3,), (4,))),
        ((1,), ((1, 1), (1, 3), (1, 4))),
        ((3,), ((3, 1), (3, 2), (3, 3))),
    ],
)
def test_get_candidate_paths(paths, expect):
    assert Explorer._get_candidate_paths(paths) == expect
