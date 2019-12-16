import pytest

from fft import Fft


@pytest.mark.parametrize('dilate, length, expect', [
    (1, 4, (1, 0, -1, 0)),
    (1, 6, (1, 0, -1, 0, 1, 0)),
    (2, 6, (0, 1, 1, 0, 0, -1)),
    (2, 9, (0, 1, 1, 0, 0, -1, -1, 0, 0)),
    (3, 12, (0, 0, 1, 1, 1, 0, 0, 0, -1, -1, -1, 0)),
])
def test_fft_get_pattern(dilate, length, expect):
    p = Fft.get_pattern(dilate, length)
    assert p == expect
