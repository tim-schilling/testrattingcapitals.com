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
import pytest
from testrattingcapitals import cache_service as unit
from testrattingcapitals.schema import TrackedKill


class MockCacheRepository(object):
    def __init__(self, to_return, *args, **kwargs):
        self.to_return = to_return
        self.called = 0

    def _super_secret_test_handler(self, method_called, called_args, called_kwargs):
        self.called = self.called + 1
        self.method_called = method_called
        self.called_with_args = called_args
        self.called_with_kwargs = called_kwargs
        return self.to_return

    def get_latest_for_label(self, *args, **kwargs):
        return self._super_secret_test_handler('get_latest_for_label', args, kwargs)

    def get_recents_for_label(self, *args, **kwargs):
        return self._super_secret_test_handler('get_recents_for_label', args, kwargs)

    def set_latest_for_label(self, *args, **kwargs):
        return self._super_secret_test_handler('set_latest_for_tracking_label', args, kwargs)

    def set_recents_for_label(self, *args, **kwargs):
        return self._super_secret_test_handler('set_recents_for_label', args, kwargs)

    def delete_expired_recents_for_label(self, *args, **kwargs):
        return self._super_secret_test_handler('delete_expired_recents_for_label', args, kwargs)


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

    unit.validate_tracked_kill_list(None)

    with pytest.raises(TypeError):
        unit.validate_tracked_kill_list(1)

    with pytest.raises(Exception):
        unit.validate_tracked_kill_list([TrackedKill(kill_id=1)])

    monkeypatch.setattr(unit, 'validate_tracked_kill', mock_validate_tracked_kill_pass)

    unit.validate_tracked_kill_list([TrackedKill(kill_id=1)])
    unit.validate_tracked_kill_list([])


def test_validate_exclusive_end_date():
    unit.validate_exclusive_end_date(None)
    unit.validate_exclusive_end_date(datetime.datetime(2017, 1, 1))

    with pytest.raises(TypeError):
        unit.validate_exclusive_end_date('fail')


def test_get_for_tracking_label(monkeypatch):
    mock_repo = MockCacheRepository('hello')
    monkeypatch.setattr(unit, 'cache_repository', mock_repo)

    result = unit.get_for_tracking_label('unittest', start_date=datetime.datetime(2017, 1, 31))
    assert 2 == mock_repo.called
    assert 'unittest' == mock_repo.called_with_args[0]
    assert datetime.datetime(2017, 1, 31).date() == mock_repo.called_with_args[1].date()
    assert isinstance(result, dict)
    assert 'hello' == result.get('latest')
    assert 'hello' == result.get('recent')

    mock_repo = MockCacheRepository('hello')
    monkeypatch.setattr(unit, 'cache_repository', mock_repo)

    result = unit.get_for_tracking_label('unittest')
    # testing a datetime.now call, be as generous as possible
    assert (datetime.datetime.utcnow() - datetime.timedelta(days=29)).date() >= mock_repo.called_with_args[1].date()
    assert (datetime.datetime.utcnow() - datetime.timedelta(days=31)).date() <= mock_repo.called_with_args[1].date()


def test_set_for_tracking_label(monkeypatch):
    mock_repo = MockCacheRepository(None)
    monkeypatch.setattr(unit, 'cache_repository', mock_repo)

    unit.set_for_tracking_label('UNITTEST', None)
    assert 2 == mock_repo.called
    assert 'UNITTEST' == mock_repo.called_with_args[0]
    assert mock_repo.called_with_args[1] is None

    mock_repo = MockCacheRepository(None)
    monkeypatch.setattr(unit, 'cache_repository', mock_repo)

    input_values = [
        TrackedKill(kill_id=1, kill_timestamp=datetime.datetime(2017, 1, 1)),
        TrackedKill(kill_id=2, kill_timestamp=datetime.datetime(2016, 12, 31)),
    ]
    unit.set_for_tracking_label('UNITTEST', input_values)

    assert 2 == mock_repo.called
    assert 'UNITTEST' == mock_repo.called_with_args[0]
    assert mock_repo.called_with_args[1] is input_values


def test_expire_recents_for_label(monkeypatch):
    mock_repo = MockCacheRepository(None)
    monkeypatch.setattr(unit, 'cache_repository', mock_repo)

    unit.expire_recents_for_label('UNITTEST')

    # testing a datetime.now call, be as generous as possible
    assert 'UNITTEST' == mock_repo.called_with_args[0]
    assert (datetime.datetime.utcnow() - datetime.timedelta(days=29)).date() >= mock_repo.called_with_args[1].date()
    assert (datetime.datetime.utcnow() - datetime.timedelta(days=31)).date() <= mock_repo.called_with_args[1].date()

    mock_repo = MockCacheRepository(None)
    monkeypatch.setattr(unit, 'cache_repository', mock_repo)

    unit.expire_recents_for_label('UNITTEST', datetime.datetime(2017, 7, 31))

    assert 'UNITTEST' == mock_repo.called_with_args[0]
    assert datetime.datetime(2017, 7, 31) == mock_repo.called_with_args[1]
