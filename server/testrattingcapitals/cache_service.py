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

from datetime import datetime, timedelta
import logging
from testrattingcapitals import cache_repository

logger = logging.getLogger('testrattingcapitals')

DEFAULT_EXPIRATION_CUTOFF_DAYS = 30


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
    if not tracked_kill_list:
        return

    if not isinstance(tracked_kill_list, list):
        raise(TypeError('tracked_kill_list'))

    for kill in tracked_kill_list:
        validate_tracked_kill(kill)


def validate_start_date(start_date):
    if start_date and not isinstance(start_date, datetime):
        raise(TypeError('start_date'))


def validate_exclusive_end_date(exclusive_end_date):
    if exclusive_end_date and not isinstance(exclusive_end_date, datetime):
        raise(TypeError('exclusive_end_date'))


def get_for_tracking_label(tracking_label, **kwargs):
    validate_tracking_label(tracking_label)

    default_start_date = datetime.utcnow() - timedelta(days=DEFAULT_EXPIRATION_CUTOFF_DAYS)
    start_date = kwargs.get('start_date', default_start_date)
    validate_start_date(kwargs.get('start_date'))

    latest = cache_repository.get_latest_for_label(tracking_label)
    recents = cache_repository.get_recents_for_label(tracking_label, start_date)

    return {
        'latest': latest,
        'recent': recents
    }


def get_latest_for_tracking_label(tracking_label):
    validate_tracking_label(tracking_label)

    return cache_repository.get_latest_for_label(tracking_label)


def set_for_tracking_label(tracking_label, tracked_kill_list):
    validate_tracking_label(tracking_label)
    validate_tracked_kill_list(tracked_kill_list)

    # find the latest
    # these come from sqlite in desc order, so it's just the first
    if tracked_kill_list and len(tracked_kill_list):
        latest = tracked_kill_list[0]
    else:
        latest = None

    cache_repository.set_latest_for_label(tracking_label, latest)
    cache_repository.set_recents_for_label(tracking_label, tracked_kill_list)


def expire_recents_for_label(tracking_label, exclusive_end_date=None):
    validate_tracking_label(tracking_label)
    validate_exclusive_end_date(exclusive_end_date)

    if not exclusive_end_date:
        exclusive_end_date = datetime.utcnow() - timedelta(days=DEFAULT_EXPIRATION_CUTOFF_DAYS)

    cache_repository.delete_expired_recents_for_label(tracking_label, exclusive_end_date)
