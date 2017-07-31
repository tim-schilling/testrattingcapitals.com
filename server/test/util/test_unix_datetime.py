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
from testrattingcapitals.util import unix_datetime as unit


def test_datetime_to_unix():
    result = unit.datetime_to_unix('fail')
    assert result is None

    result = unit.datetime_to_unix(
        datetime.datetime(2017, 7, 30, 20, 0, 0, tzinfo=datetime.timezone.utc)
    )
    assert 1501444800 == result


def test_unix_to_datetime():
    result = unit.unix_to_datetime('fail')
    assert result is None

    result = unit.unix_to_datetime(1501444800)
    assertion = datetime.datetime(2017, 7, 30, 20, 0, 0, tzinfo=datetime.timezone.utc)
    assert assertion == result
