import pytest

from fft import Fft


@pytest.mark.parametrize('dilate, length, expect', [
    (1, 2, (1, 0)),
    (1, 4, (1, 0, -1, 0)),
    (1, 6, (1, 0, -1, 0, 1, 0)),
    (2, 6, (0, 1, 1, 0, 0, -1)),
    (2, 9, (0, 1, 1, 0, 0, -1, -1, 0, 0)),
    (3, 12, (0, 0, 1, 1, 1, 0, 0, 0, -1, -1, -1, 0)),
])
def test_fft_get_pattern(dilate, length, expect):
    p = Fft.get_pattern(dilate, length)
    assert p == expect


@pytest.mark.parametrize('input, expect', [
    ('80871224585914546619083218645595', '24176176'),
    ('19617804207202209144916044189917', '73745418'),
    ('69317163492948606335995924319873', '52432133'),
])
def test_fft_advance(input, expect):
    computer = Fft(input)
    computer.advance_n(100)
    assert expect == computer.get_state()[:8]
