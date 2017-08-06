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

from testrattingcapitals import zkrq_repository

logger = logging.getLogger('testrattingcapitals')


def get(queue_id=None, time_to_wait=None):
    logger.debug('Service querying zkrq')
    validate_queue_id(queue_id)
    validate_time_to_wait(time_to_wait)

    params = {}
    if queue_id:
        params['queueID'] = queue_id
    if time_to_wait:
        params['ttw'] = time_to_wait

    headers = {}
    if os.getenv('ZKRQ_USER_AGENT'):
        headers['User-Agent'] = os.getenv('ZKRQ_USER_AGENT')

    response = zkrq_repository.get(params, headers)
    response.raise_for_status()

    parsed_response = response.json()
    if parsed_response['package'] is None:
        logger.debug('zkrq returned no kill')
        return None
    logger.debug('f{parsed_response['package']['killID']} zkrq returned')
    return parsed_response


def validate_queue_id(queue_id):
    if isinstance(queue_id, str):
        if queue_id == '' or ' ' in queue_id:
            raise ValueError('queue_id')
        return
    if queue_id is not None:
        raise TypeError('queue_id')


def validate_time_to_wait(time_to_wait):
    if not isinstance(time_to_wait, int):
        raise TypeError('time_to_wait')
    if 0 >= time_to_wait > 10:
        raise ValueError('time_to_wait')
