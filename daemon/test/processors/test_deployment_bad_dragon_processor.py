from datetime import datetime
from processors import deployment_bad_dragon_processor as unit, shared_defines


def test_process_ok():
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
                        'id': shared_defines.TEST_ALLIANCE_ID
                    }
                }
            }
        }
    }

    result = unit.process(test_input)
    assert isinstance(result, str)


def test_process_wrong_alliance():
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
                        'id': shared_defines.TEST_ALLIANCE_ID + 1
                    }
                }
            }
        }
    }

    result = unit.process(test_input)
    assert result is None


def test_process_no_alliance():
    test_input = {
        'package': {
            'killID': 1,
            'killmail': {
                'killTime': '2017.07.24 01:01:01',
                'solarSystem': {
                    'name': 'D-PNP9'
                },
                'victim': {
                }
            }
        }
    }

    result = unit.process(test_input)
    assert result is None


def test_process_before_startdate(monkeypatch):
    monkeypatch.setattr(unit, 'START_TIMESTAMP', datetime(2020, 1, 1))
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
                        'id': shared_defines.TEST_ALLIANCE_ID
                    }
                }
            }
        }
    }

    result = unit.process(test_input)
    assert result is None


def test_process_no_startdate(monkeypatch):
    monkeypatch.setattr(unit, 'START_TIMESTAMP', None)
    test_input = {
        'package': {
            'killID': 1,
            'killmail': {
                'killTime': '1990.07.24 01:01:01',
                'solarSystem': {
                    'name': 'D-PNP9'
                },
                'victim': {
                    'alliance': {
                        'id': shared_defines.TEST_ALLIANCE_ID
                    }
                }
            }
        }
    }

    result = unit.process(test_input)
    assert isinstance(result, str)


def test_process_after_startdate(monkeypatch):
    monkeypatch.setattr(unit, 'START_TIMESTAMP', datetime(2000, 1, 1))
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
                        'id': shared_defines.TEST_ALLIANCE_ID
                    }
                }
            }
        }
    }

    result = unit.process(test_input)
    assert isinstance(result, str)


def test_process_after_enddate(monkeypatch):
    monkeypatch.setattr(unit, 'START_TIMESTAMP', datetime(2000, 1, 1))
    monkeypatch.setattr(unit, 'END_TIMESTAMP', datetime(2001, 1, 1))
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
                        'id': shared_defines.TEST_ALLIANCE_ID
                    }
                }
            }
        }
    }

    result = unit.process(test_input)
    assert result is None


def test_process_no_enddate(monkeypatch):
    monkeypatch.setattr(unit, 'START_TIMESTAMP', datetime(2000, 1, 1))
    monkeypatch.setattr(unit, 'END_TIMESTAMP', None)
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
                        'id': shared_defines.TEST_ALLIANCE_ID
                    }
                }
            }
        }
    }

    result = unit.process(test_input)
    assert isinstance(result, str)


def test_process_before_enddate(monkeypatch):
    monkeypatch.setattr(unit, 'START_TIMESTAMP', datetime(2000, 1, 1))
    monkeypatch.setattr(unit, 'END_TIMESTAMP', datetime(2020, 1, 1))
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
                        'id': shared_defines.TEST_ALLIANCE_ID
                    }
                }
            }
        }
    }

    result = unit.process(test_input)
    assert isinstance(result, str)


def test_process_is_in_esoteria(monkeypatch):
    monkeypatch.setattr(unit, 'START_TIMESTAMP', datetime(2000, 1, 1))
    monkeypatch.setattr(unit, 'END_TIMESTAMP', datetime(2020, 1, 1))
    monkeypatch.setattr(unit, 'ESOTERIA_SYSTEM_NAMES', {'D-PNP9'})
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
                        'id': shared_defines.TEST_ALLIANCE_ID
                    }
                }
            }
        }
    }

    result = unit.process(test_input)
    assert isinstance(result, str)


def test_process_is_not_in_esoteria(monkeypatch):
    monkeypatch.setattr(unit, 'START_TIMESTAMP', datetime(2000, 1, 1))
    monkeypatch.setattr(unit, 'END_TIMESTAMP', datetime(2020, 1, 1))
    monkeypatch.setattr(unit, 'ESOTERIA_SYSTEM_NAMES', {'not D-PNP9'})
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
                        'id': shared_defines.TEST_ALLIANCE_ID
                    }
                }
            }
        }
    }

    result = unit.process(test_input)
    assert result is None
