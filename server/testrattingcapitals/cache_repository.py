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
from testrattingcapitals.util import unix_datetime
from testrattingcapitals.schema import TrackedKill

LATEST_KEY_FORMAT = 'LATEST_{}'
RECENT_KEY_FORMAT = 'RECENT_{}'


def get_latest_for_label(label):
    conn = redis.get_redis_singleton()
    response = conn.get(LATEST_KEY_FORMAT.format(label))
    if response:
        return TrackedKill.from_json(response)
    else:
        return None


def set_latest_for_label(label, value):
    conn = redis.get_redis_singleton()
    if value:
        value_as_json = TrackedKill.to_json(value)
        conn.set(LATEST_KEY_FORMAT.format(label), value_as_json)
    else:
        conn.delete(LATEST_KEY_FORMAT.format(label))


def get_recents_for_label(label, start_date):
    conn = redis.get_redis_singleton()

    start_date_score = unix_datetime.datetime_to_unix(start_date)

    response = conn.zrevrangebyscore(
        RECENT_KEY_FORMAT.format(label),
        '+inf',
        start_date_score
    ) or []

    for index, value in enumerate(response):
        response[index] = TrackedKill.from_json(response[index])

    return response


def set_recents_for_label(label, values):
    conn = redis.get_redis_singleton()

    key = RECENT_KEY_FORMAT.format(label)
    for value in values or []:
        score = unix_datetime.datetime_to_unix(value.kill_timestamp)
        value_as_json = TrackedKill.to_json(value)
        conn.zadd(key, score, value_as_json)


def delete_expired_recents_for_label(label, exclusive_end_date):
    conn = redis.get_redis_singleton()

    key = RECENT_KEY_FORMAT.format(label)
    score_cutoff = '({}'.format(unix_datetime.datetime_to_unix(exclusive_end_date))

    conn.zremrangebyscore(key, '-inf', score_cutoff)
