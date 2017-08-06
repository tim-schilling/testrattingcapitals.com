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

from datetime import datetime
import json
import logging

from testrattingcapitals import tracked_kill_repository
from testrattingcapitals.schema import TrackedKill

logger = logging.getLogger('testrattingcapitals')


def add(tracking_label, zk_response):
    """Add a kill to the database with the passed tracking_label.
    """
    # validate input
    validate_tracking_label(tracking_label)
    validate_zk_response(zk_response)

    # convert input to a database model
    tk = convert_zk_response_to_tracked_kill(tracking_label, zk_response)

    # persist instance
    logger.debug('{}-{} service persisting'.format(tk.kill_id, tk.kill_tracking_label))
    tracked_kill_repository.add(tk)


def get(tracking_label=None):
    """Retrieve all records, optionally filtering by tracking_label.
    """
    if tracking_label:
        validate_tracking_label(tracking_label)

    return tracked_kill_repository.get(tracking_label)


def get_since(tracking_label, start_date):
    """Retrieve all kills for a tracking_label since start_date.
    """
    logger.debug('{}-{} service querying get_since'.format(
        tracking_label,
        start_date
    ))
    validate_tracking_label(tracking_label)
    validate_start_date(start_date)

    return tracked_kill_repository.get_since(tracking_label, start_date)


def validate_tracking_label(tracking_label):
    if not isinstance(tracking_label, str):
        raise TypeError('tracking_label')
    if tracking_label == '':
        raise ValueError('tracking_label')


def validate_start_date(start_date):
    if not isinstance(start_date, datetime):
        raise(TypeError('start_date'))


def validate_zk_response(zk_response):
    if not isinstance(zk_response, dict):
        raise(TypeError('zk_response'))


def convert_zk_timestamp_to_datetime(zk_timestamp):
    if not isinstance(zk_timestamp, str):
        return None
    return datetime.strptime(zk_timestamp, '%Y.%m.%d %H:%M:%S')


def convert_zk_response_to_tracked_kill(tracking_label, zk):
    """Convert zk response dict to a TrackedKill instance
    """
    
    # Should this be an and?
    if not isinstance(tracking_label, str) or not isinstance(zk, dict):
        return None

    pk = zk['package']

    tk = TrackedKill()
    tk.kill_tracking_label = tracking_label
    tk.kill_id = pk['killID']
    tk.kill_timestamp = convert_zk_timestamp_to_datetime(
        pk['killmail']['killTime']
    )
    tk.ship_id = pk['killmail']['victim']['shipType']['id']
    # structure kills do not have an associated character
    if 'character' in pk['killmail']['victim']:
        tk.character_id = pk['killmail']['victim']['character']['id']
    tk.corporation_id = pk['killmail']['victim']['corporation']['id']
    # players do not have to join an alliance
    if 'alliance' in pk['killmail']['victim']:
        tk.alliance_id = pk['killmail']['victim']['alliance']['id']
    tk.total_value = pk['zkb']['totalValue']
    tk.system_id = pk['killmail']['solarSystem']['id']
    tk.more_info_href = 'https://zkillboard.com/kill/{}/'.format(pk['killID'])
    tk.full_response = json.dumps(zk)

    tk.character_name = None  # deprecated
    tk.corporation_name = ''  # deprecated
    tk.alliance_name = None  # deprecated
    tk.ship_name = ''  # deprecated
    tk.system_name = ''  # deprecated

    return tk
