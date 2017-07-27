"""
  Copyright (c) 2016-2017 Tony Lechner and contributors

  testrattingcapitals.com is free software: you can redistribute it and/or
  modify it under the terms of the GNU Affero General Public License as
  published by the Free Software Foundation, either version 3 of the
  License, or (at your option) any later version.

  testrattingcapitals.com is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU Affero General Public License for more details.

  You should have received a copy of the GNU Affero General Public License
  along with testrattingcapitals.com.  If not, see
  <http://www.gnu.org/licenses/>.
"""

from testrattingcapitals.processors import ratting_capital_processor as unit, shared_defines

mock_ship_id_set = {1, 2, 3}


def test_process_ok(monkeypatch):
    monkeypatch.setattr(unit, 'RATTING_CAPITAL_SHIP_IDS', mock_ship_id_set)
    test_input = {
        'package': {
            'killID': 1,
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
            'killID': 1,
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
            'killID': 1,
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
            'killID': 1,
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
