from processors import ratting_capital_processor as unit, shared_defines

mock_ship_id_set = {1, 2, 3}


def test_process_ok(monkeypatch):
    monkeypatch.setattr(unit, 'RATTING_CAPITAL_SHIP_IDS', mock_ship_id_set)
    test_input = {
        'package': {
            'killmail': {
                'victim': {
                    'alliance': {
                        'id': shared_defines.TEST_ALLIANCE_ID
                    },
                    'shipType': {
                        'id':  1
                    }
                }
            }
        }
    }

    result = unit.process(test_input)
    assert isinstance(result, str)


def test_process_wrong_alliance(monkeypatch):
    monkeypatch.setattr(unit, 'RATTING_CAPITAL_SHIP_IDS', mock_ship_id_set)
    test_input = {
        'package': {
            'killmail': {
                'victim': {
                    'alliance': {
                        'id': shared_defines.TEST_ALLIANCE_ID + 1
                    },
                    'shipType': {
                        'id':  1
                    }
                }
            }
        }
    }

    result = unit.process(test_input)
    assert result is None


def test_process_no_alliance(monkeypatch):
    monkeypatch.setattr(unit, 'RATTING_CAPITAL_SHIP_IDS', mock_ship_id_set)
    test_input = {
        'package': {
            'killmail': {
                'victim': {
                    'shipType': {
                        'id':  1
                    }
                }
            }
        }
    }

    result = unit.process(test_input)
    assert result is None


def test_process_wrong_ship_id(monkeypatch):
    monkeypatch.setattr(unit, 'RATTING_CAPITAL_SHIP_IDS', mock_ship_id_set)
    test_input = {
        'package': {
            'killmail': {
                'victim': {
                    'alliance': {
                        'id': shared_defines.TEST_ALLIANCE_ID
                    },
                    'shipType': {
                        'id':  5
                    }
                }
            }
        }
    }

    result = unit.process(test_input)
    assert result is None
