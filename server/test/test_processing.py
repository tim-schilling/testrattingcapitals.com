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

from testrattingcapitals import processing as unit


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
