from processors import all_processor as unit


def test_process():
    assert unit.process(None) is None
    assert isinstance(unit.process(dict()), str)
