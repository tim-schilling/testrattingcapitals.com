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

from testrattingcapitals import redis as unit


class MockStrictRedis(object):
    def __init__(self, url):
        self.url = url

    def ping(self):
        pass

    @staticmethod
    def from_url(url, *args, **kwargs):
        return MockStrictRedis('unit-test-url')


def setup_module(module):
    module.unit._singleton = None


def teardown_module(module):
    module.unit._singleton = None


def test_singleton_behavior(monkeypatch):
    monkeypatch.setattr(unit, 'StrictRedis', MockStrictRedis)
    first_ref = unit.get_redis_singleton()
    second_ref = unit.get_redis_singleton()
    assert first_ref is second_ref
