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

import os
import pytest

from testrattingcapitals import zkrq_repository, zkrq_service as unit


def test_validate_queue_id():
    # string not emptystring
    with pytest.raises(ValueError):
        unit.validate_queue_id('')

    # string has no spaces
    with pytest.raises(ValueError):
        unit.validate_queue_id('f a i l')

    # string otherwise acceptible
    unit.validate_queue_id('valid')

    # None acceptible
    unit.validate_queue_id(None)

    # other types invalid
    with pytest.raises(TypeError):
        unit.validate_queue_id(1)

    with pytest.raises(TypeError):
        unit.validate_queue_id(1.1)

    with pytest.raises(TypeError):
        unit.validate_queue_id({})


def test_validate_time_to_wait():
    # int not 0
    with pytest.raises(ValueError):
        unit.validate_time_to_wait(0)

    # int not < 0
    with pytest.raises(ValueError):
        unit.validate_time_to_wait(-1)

    with pytest.raises(ValueError):
        unit.validate_time_to_wait(-30)

    # positive int acceptible
    unit.validate_time_to_wait(1)
    unit.validate_time_to_wait(10)

    # None acceptible
    unit.validate_time_to_wait(None)


class MockResponse(object):
    def __init__(self, content, status_code):
        self.content = content
        self.status_code = status_code

    def json(self):
        return self.content

    def raise_for_status(self):
        if self.status_code != 200:
            raise Exception('mock response status code != 200')


def test_get_params_object(monkeypatch):
    def mock_repo_get(params={}, headers={}):
        assert 'queueID' in params
        assert 'ttw' in params
        assert 'a' == params['queueID']
        assert 9 == params['ttw']

        return MockResponse({'package': {'unit': 'test', 'killID': 1}}, 200)

    monkeypatch.setattr(zkrq_repository, 'get', mock_repo_get)

    unit.get('a', 9)


def test_get_header_object(monkeypatch):
    def mock_getenv(*args, **kwargs):
        return 'mock user agent'

    def mock_repo_get(params={}, headers={}):
        assert 'queueID' in params
        assert 'ttw' in params
        assert 'a' == params['queueID']
        assert 9 == params['ttw']
        assert 'User-Agent' in headers
        assert 'mock user agent' == headers['User-Agent']

        return MockResponse({'package': {'unit': 'test', 'killID': 1}}, 200)

    monkeypatch.setattr(os, 'getenv', mock_getenv)
    monkeypatch.setattr(zkrq_repository, 'get', mock_repo_get)

    unit.get('a', 9)


def test_get_200_with_body(monkeypatch):
    def mock_repo_get(params={}, headers={}):
        return MockResponse({'package': {'unit': 'test', 'killID': 1}}, 200)

    monkeypatch.setattr(zkrq_repository, 'get', mock_repo_get)

    response = unit.get()
    assert 'package' in response
    assert 'unit' in response['package']
    assert 'test' == response['package']['unit']


def test_get_200_with_no_body(monkeypatch):
    def mock_repo_get(params={}, headers={}):
        return MockResponse({'package': None}, 200)

    monkeypatch.setattr(zkrq_repository, 'get', mock_repo_get)

    response = unit.get()
    assert response is None


def test_get_500(monkeypatch):
    def mock_repo_get(params={}, headers={}):
        return MockResponse(None, 500)

    monkeypatch.setattr(zkrq_repository, 'get', mock_repo_get)

    with pytest.raises(Exception):
        unit.get()
