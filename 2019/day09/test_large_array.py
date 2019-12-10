from large_array import LargeArray


def test_large_array():
    sut = LargeArray([1, 2, 3])
    assert sut[0] == 1
    assert sut[1] == 2
    assert sut[2] == 3
    assert sut[3] == 0
    sut[3] = 4
    assert sut[3] == 4
    sut[1000001] = 42
    assert sut[1000001] == 42
