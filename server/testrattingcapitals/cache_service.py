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

import json
import logging
from testrattingcapitals.schema import AlchemyEncoder, TrackedKill

logger = logging.getLogger('testrattingcapitals')


def validate_tracking_label(tracking_label):
    if not isinstance(tracking_label, str):
        raise(TypeError('tracking_label'))
    if tracking_label == '':
        raise(ValueError('tracking_label'))


def validate_tracked_kill(tracked_kill):
    if not tracked_kill:
        raise(TypeError('tracked_kill'))

    if not tracked_kill.kill_id:
        raise(ValueError('tracked_kill'))


def validate_tracked_kill_list(tracked_kill_list):
    if not isinstance(tracked_kill_list, list):
        raise(TypeError('tracked_kill_list'))

    for kill in tracked_kill_list:
        validate_tracked_kill(kill)


def dict_to_tracked_kill(kill_dict):
    if not isinstance(kill_dict, dict):
        raise(TypeError('kill_dict'))

    return TrackedKill(**kill_dict)


def json_to_tracked_kill(kill_json):
    if not isinstance(kill_json, str):
        raise(TypeError('kill_json'))

    return TrackedKill(**json.loads(kill_json))


def tracked_kill_to_json(tracked_kill):
    if not tracked_kill:
        raise(TypeError('tracked_kill'))

    return json.dumps(tracked_kill, cls=AlchemyEncoder)
