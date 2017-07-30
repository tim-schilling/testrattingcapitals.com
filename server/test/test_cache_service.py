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

import json
import pytest
from testrattingcapitals import cache_service as unit
from testrattingcapitals.schema import TrackedKill


def test_validate_tracking_label():
    with pytest.raises(TypeError):
        unit.validate_tracking_label(1234)

    with pytest.raises(TypeError):
        unit.validate_tracking_label(None)

    with pytest.raises(ValueError):
        unit.validate_tracking_label('')

    unit.validate_tracking_label('valid')


def test_validate_tracked_kill():
    with pytest.raises(TypeError):
        unit.validate_tracked_kill(None)

    with pytest.raises(ValueError):
        unit.validate_tracked_kill(TrackedKill())

    unit.validate_tracked_kill(TrackedKill(kill_id=1))


def test_validate_tracked_kill_list(monkeypatch):
    def mock_validate_tracked_kill_pass(*args, **kwargs):
        pass

    def mock_validate_tracked_kill_fail(*args, **kwargs):
        raise Exception('unit test')

    monkeypatch.setattr(unit, 'validate_tracked_kill', mock_validate_tracked_kill_fail)

    with pytest.raises(TypeError):
        unit.validate_tracked_kill_list(None)

    with pytest.raises(TypeError):
        unit.validate_tracked_kill_list(1)

    with pytest.raises(Exception):
        unit.validate_tracked_kill_list([TrackedKill(kill_id=1)])

    monkeypatch.setattr(unit, 'validate_tracked_kill', mock_validate_tracked_kill_pass)

    unit.validate_tracked_kill_list([TrackedKill(kill_id=1)])
    unit.validate_tracked_kill_list([])


def test_json_to_tracked_kill():
    with pytest.raises(TypeError):
        unit.json_to_tracked_kill(None)

    result = unit.json_to_tracked_kill('{"kill_id":105,"kill_tracking_label":"UNIT TEST"}')
    assert isinstance(result, TrackedKill)
    assert 105 == result.kill_id
    assert 'UNIT TEST' == result.kill_tracking_label


def test_tracked_kill_to_json():
    with pytest.raises(TypeError):
        unit.tracked_kill_to_json(None)

    result = unit.tracked_kill_to_json(TrackedKill(kill_id=102, kill_tracking_label='unit test'))
    assert isinstance(result, str)
    assert '{"kill_id":102,"kill_tracking_label":"unit test"}'


def test_get_latest_tracked_kill_for_tracking_label(monkeypatch):
    def mock_repo_get(*args, **kwargs):
        return '{"kill_id":5,"kill_tracking_label":"hi"}'

    monkeypatch.setattr(unit.cache_repository, 'get_latest_for_label', mock_repo_get)

    result = unit.get_latest_tracked_kill_for_tracking_label('hi')
    assert 5 == result.kill_id
    assert 'hi' == result.kill_tracking_label


def test_set_latest_tracked_kill_for_tracking_label(monkeypatch):
    mock_set_label = ''
    mock_set_kill = None

    def mock_repo_set(tracking_label, tracked_kill):
        nonlocal mock_set_label, mock_set_kill
        mock_set_label = tracking_label
        mock_set_kill = tracked_kill

    monkeypatch.setattr(unit.cache_repository, 'set_latest_for_label', mock_repo_set)
    unit.set_latest_tracked_kill_for_tracking_label('some label', TrackedKill(kill_id=3))
    assert 3 == json.loads(mock_set_kill).get('kill_id')
    assert 'some label' == mock_set_label


def test_get_recent_tracked_kills_for_tracking_label(monkeypatch):
    def mock_repo_get(tracking_label):
        return json.dumps([{'kill_tracking_label': tracking_label}])

    monkeypatch.setattr(unit.cache_repository, 'get_recents_for_label', mock_repo_get)

    result = unit.get_recent_tracked_kills_for_tracking_label('hello')
    assert result[0]
    assert 'hello' == result[0].kill_tracking_label


def test_set_recent_tracked_kills_for_tracking_label(monkeypatch):
    mock_set_label = ''
    mock_set_list = []

    def mock_repo_set(tracking_label, tracked_kill_list):
        nonlocal mock_set_label, mock_set_list
        mock_set_label = tracking_label
        mock_set_list = tracked_kill_list

    monkeypatch.setattr(unit.cache_repository, 'set_recents_for_label', mock_repo_set)

    input_list = [
        TrackedKill(kill_id=1),
        TrackedKill(kill_id=2),
    ]

    unit.set_recent_tracked_kills_for_tracking_label('a_label', input_list)
    assert 'a_label' == mock_set_label
    assert isinstance(mock_set_list, str)
    as_json = json.loads(mock_set_list)
    assert isinstance(as_json, list)
    assert 1 == as_json[0].get('kill_id')
    assert 2 == as_json[1].get('kill_id')
