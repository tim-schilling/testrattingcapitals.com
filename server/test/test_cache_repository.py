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

import datetime
from testrattingcapitals import cache_repository as unit
from testrattingcapitals.schema import TrackedKill


class MockRedisDispenser(object):
    def __init__(self, to_dispense):
        self.to_dispense = to_dispense

    def get_redis_singleton(self):
        return self.to_dispense


class MockRedis(object):
    def __init__(self, to_return, *args, **kwargs):
        self.to_return = to_return
        self.called = 0

    def _super_secret_test_handler(self, method_called, called_args, called_kwargs):
        self.called = self.called + 1
        self.method_called = method_called
        self.called_with_args = called_args
        self.called_with_kwargs = called_kwargs
        return self.to_return

    def get(self, *args, **kwargs):
        return self._super_secret_test_handler('get', args, kwargs)

    def set(self, *args, **kwargs):
        return self._super_secret_test_handler('set', args, kwargs)

    def delete(self, *args, **kwargs):
        return self._super_secret_test_handler('delete', args, kwargs)

    def zadd(self, *args, **kwargs):
        return self._super_secret_test_handler('zadd', args, kwargs)

    def zremrangebyscore(self, *args, **kwargs):
        return self._super_secret_test_handler('zremrangebyscore', args, kwargs)

    def zrevrangebyscore(self, *args, **kwargs):
        return self._super_secret_test_handler('zrevrangebyscore', args, kwargs)


def test_get_latest_for_label(monkeypatch):
    mock_redis_instance = MockRedis(None)
    monkeypatch.setattr(unit, 'redis', MockRedisDispenser(mock_redis_instance))

    result = unit.get_latest_for_label('RETURNS_NOTHING')
    assert 'get' == mock_redis_instance.method_called
    assert 'LATEST_RETURNS_NOTHING' == mock_redis_instance.called_with_args[0]
    assert result is None

    mock_redis_instance = MockRedis(TrackedKill.to_json(TrackedKill(kill_id=500)))
    monkeypatch.setattr(unit, 'redis', MockRedisDispenser(mock_redis_instance))

    result = unit.get_latest_for_label('RETURNS_SOMETHING')
    assert 'get' == mock_redis_instance.method_called
    assert 'LATEST_RETURNS_SOMETHING' == mock_redis_instance.called_with_args[0]
    assert isinstance(result, TrackedKill)
    assert 500 == result.kill_id


def test_set_latest_for_label(monkeypatch):
    mock_redis_instance = MockRedis(None)
    monkeypatch.setattr(unit, 'redis', MockRedisDispenser(mock_redis_instance))
    unit.set_latest_for_label('DELETES', None)
    assert 'delete' == mock_redis_instance.method_called
    assert 'LATEST_DELETES' == mock_redis_instance.called_with_args[0]

    mock_redis_instance = MockRedis(None)
    monkeypatch.setattr(unit, 'redis', MockRedisDispenser(mock_redis_instance))
    a_kill = TrackedKill(kill_id=1000)
    unit.set_latest_for_label('SETS', a_kill)
    assert 'set' == mock_redis_instance.method_called
    assert 'LATEST_SETS' == mock_redis_instance.called_with_args[0]
    assert 1000 == TrackedKill.from_json(mock_redis_instance.called_with_args[1]).kill_id


def test_get_recents_for_label(monkeypatch):
    mock_redis_instance = MockRedis([
        TrackedKill.to_json(TrackedKill(kill_id=7)),
        TrackedKill.to_json(TrackedKill(kill_id=8)),
    ])
    monkeypatch.setattr(unit, 'redis', MockRedisDispenser(mock_redis_instance))
    result = unit.get_recents_for_label(
        'UNITTEST',
        datetime.datetime(2017, 7, 30, 20, 0, 0, tzinfo=datetime.timezone.utc)
    )
    assert 'zrevrangebyscore' == mock_redis_instance.method_called
    assert 'RECENT_UNITTEST' == mock_redis_instance.called_with_args[0]
    assert '+inf' == mock_redis_instance.called_with_args[1]
    assert 1501444800 == mock_redis_instance.called_with_args[2]
    assert isinstance(result, list)
    assert 2 == len(result)
    assert 7 == result[0].kill_id
    assert 8 == result[1].kill_id


def test_set_recents_for_label(monkeypatch):
    mock_redis_instance = MockRedis(None)
    monkeypatch.setattr(unit, 'redis', MockRedisDispenser(mock_redis_instance))

    input_values = [
        TrackedKill(kill_id=8, kill_timestamp=datetime.datetime(2017, 7, 30, 20, 0, 0, tzinfo=datetime.timezone.utc)),
    ]
    unit.set_recents_for_label('UNITTEST', input_values)
    assert 'zadd' == mock_redis_instance.method_called
    assert 1 == mock_redis_instance.called
    assert 'RECENT_UNITTEST' == mock_redis_instance.called_with_args[0]
    assert 1501444800 == mock_redis_instance.called_with_args[1]
    assert TrackedKill.to_json(input_values[0]) == mock_redis_instance.called_with_args[2]

    mock_redis_instance = MockRedis(None)
    monkeypatch.setattr(unit, 'redis', MockRedisDispenser(mock_redis_instance))

    input_values = [
        TrackedKill(kill_id=8, kill_timestamp=datetime.datetime(2017, 7, 30, 20, 0, 0, tzinfo=datetime.timezone.utc)),
        TrackedKill(kill_id=9, kill_timestamp=datetime.datetime(2017, 7, 30, 20, 0, 1, tzinfo=datetime.timezone.utc)),
    ]
    unit.set_recents_for_label('UNITTEST', input_values)
    assert 2 == mock_redis_instance.called
    assert 1501444801 == mock_redis_instance.called_with_args[1]
    assert TrackedKill.to_json(input_values[1]) == mock_redis_instance.called_with_args[2]


def test_delete_expired_recents_for_label(monkeypatch):
    mock_redis_instance = MockRedis(None)
    monkeypatch.setattr(unit, 'redis', MockRedisDispenser(mock_redis_instance))

    input_exclusive_end_date = datetime.datetime(2017, 7, 30, 20, 0, 0, tzinfo=datetime.timezone.utc)

    unit.delete_expired_recents_for_label('TEST_EXPIRATION', input_exclusive_end_date)

    assert 'zremrangebyscore' == mock_redis_instance.method_called
    assert 'RECENT_TEST_EXPIRATION' == mock_redis_instance.called_with_args[0]
    assert '-inf' == mock_redis_instance.called_with_args[1]
    assert '(1501444800' == mock_redis_instance.called_with_args[2]
