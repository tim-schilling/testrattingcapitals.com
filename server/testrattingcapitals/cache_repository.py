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

from testrattingcapitals import redis


def get_latest_for_label(label):
    conn = redis.get_redis_singleton()

    response = conn.get('LATEST_{}'.format(label))
    return response


def set_latest_for_label(label, latest):
    conn = redis.get_redis_singleton()

    key_to_write = 'LATEST_{}'.format(label)
    value_to_write = None
    if latest:
        value_to_write = latest
    else:
        value_to_write = '[]'

    conn.set(key_to_write, value_to_write)


def get_recents_for_label(label):
    conn = redis.get_redis_singleton()

    response = conn.get('RECENTS_{}'.format(label))
    return response


def set_recents_for_label(label, recent_set=[]):
    conn = redis.get_redis_singleton()

    key_to_write = 'RECENTS_{}'.format(label)
    value_to_write = None
    if recent_set:
        value_to_write = recent_set
    else:
        value_to_write = []

    conn.set(key_to_write, value_to_write)
