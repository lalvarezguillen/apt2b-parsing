from apt2b.helpers import try_float_cast


def test_try_float_cast():
    cases = [("2", 2.0), ("0", 0.0), ([], None), ("t", None)]

    for inp, out in cases:
        assert try_float_cast(inp) == out

