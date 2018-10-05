from apt2b.helpers import try_float_cast, read_batch


def test_try_float_cast():
    cases = [("2", 2.0), ("0", 0.0), ([], None), ("t", None)]

    for inp, out in cases:
        assert try_float_cast(inp) == out


def test_read_batch():
    source = range(500)

    for idx, batch in enumerate(read_batch(source, batch_size=100), start=1):
        assert len(batch) == 100
    assert idx == 5
