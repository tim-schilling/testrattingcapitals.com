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
from testrattingcapitals import cache_repository
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


def get_latest_tracked_kill_for_tracking_label(tracking_label):
    logger.debug('cacher service get latest - {}'.format(tracking_label))
    validate_tracking_label(tracking_label)

    response = cache_repository.get_latest_for_label(tracking_label)
    if response:
        return json_to_tracked_kill(response)
    else:
        return None


def set_latest_tracked_kill_for_tracking_label(tracking_label, tracked_kill):
    logger.debug('cacher service set latest - {} - {}'.format(
        tracking_label,
        tracked_kill
    ))
    validate_tracking_label(tracking_label)
    validate_tracked_kill(tracked_kill)

    as_json = tracked_kill_to_json(tracked_kill)
    cache_repository.set_latest_for_label(tracking_label, as_json)


def get_recent_tracked_kills_for_tracking_label(tracking_label):
    logger.debug('cacher service.get recent - {}'.format(tracking_label))
    validate_tracking_label(tracking_label)

    response = cache_repository.get_recents_for_label(tracking_label)
    if response:
        result = []
        list_json_objects = json.loads(response)
        response = None
        while list_json_objects:
            result.append(
                dict_to_tracked_kill(
                    list_json_objects.pop(0)
                )
            )
        return result
    else:
        return []


def set_recent_tracked_kills_for_tracking_label(tracking_label, tracked_kill_list):
    logger.debug('cacher service.set recent - {} - {}'.format(
        tracking_label,
        tracked_kill_list
    ))
    validate_tracking_label(tracking_label)
    validate_tracked_kill_list(tracked_kill_list)

    as_json = tracked_kill_to_json(tracked_kill_list)
    cache_repository.set_recents_for_label(tracking_label, as_json)
