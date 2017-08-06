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

import calendar
import datetime
import pytz


def datetime_to_unix(datetime_value):
    if not isinstance(datetime_value, datetime.datetime):
        return None

    return calendar.timegm(datetime_value.utctimetuple())


def unix_to_datetime(unix_timestamp):
    if not isinstance(unix_timestamp, int):
        return None

    return pytz.UTC.localize(datetime.datetime.utcfromtimestamp(unix_timestamp))
