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

import logging
import os
from redis import StrictRedis

DEFAULT_REDIS_CONNECTION_STRING = 'redis://localhost:6379/0'

logger = logging.getLogger('testrattingcapitals')

_singleton = None


def get_redis_singleton():
    global _singleton
    if not _singleton:
        logger.debug('Redis connection pool initializing')
        _singleton = StrictRedis.from_url(
            os.getenv('REDIS_CONNECTION_STRING', DEFAULT_REDIS_CONNECTION_STRING),
            decode_responses=True
        )
        _singleton.ping()
        logger.info('Redis connection pool initialized')
    return _singleton
