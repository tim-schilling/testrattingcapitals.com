import processing as unit


def mock_processor_ok(zkill):
    return 'UNIT_TEST'


def mock_processor_ok_2(zkill):
    return 'UNIT_TEST_2'


def mock_processor_none(zkill):
    return None


def test_process(monkeypatch):
    monkeypatch.setattr(unit, 'PROCESSORS', [
        mock_processor_ok,
        mock_processor_ok_2,
        mock_processor_none,
    ])
    test_input = {
        'package': {
            'killID': 1,
            'killmail': {
                'killTime': '2017.07.24 01:01:01',
                'solarSystem': {
                    'name': 'D-PNP9'
                },
                'victim': {
                    'alliance': {
                        'id': 1
                    }
                }
            }
        }
    }
    result = unit.process(test_input)

    assert isinstance(result, set)
    assert len(result) == 2
    assert 'UNIT_TEST' in result
    assert 'UNIT_TEST_2' in result
