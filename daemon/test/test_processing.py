import processing as unit


def mock_processor_ok(zkill):
    return 'UNIT_TEST'


def mock_processor_none(zkill):
    return None


def test_process(monkeypatch):
    monkeypatch.setattr(unit, 'PROCESSORS', [mock_processor_ok, mock_processor_none])
    result = unit.process('whatever')

    assert isinstance(result, set)
    assert len(result) == 1
    assert 'UNIT_TEST' in result
