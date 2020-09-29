from app import decode


def test_example_1():
    raw_data = "0222112222120000"
    decoded = decode(raw_data, 2, 2)
    assert decoded == [[0, 1], [1, 0]]
