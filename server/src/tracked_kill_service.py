from datetime import datetime
import json
import logging
from schema import TrackedKill
import tracked_kill_repository

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


def validate_tracking_label(tracking_label):
    if not isinstance(tracking_label, str):
        raise(TypeError('tracking_label'))
    if tracking_label == '':
        raise(ValueError('tracking_label'))


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
    if not isinstance(tracking_label, str) or not isinstance(zk, dict):
        return None

    pk = zk['package']

    tk = TrackedKill()
    tk.kill_tracking_label = tracking_label
    tk.kill_id = pk['killID']
    tk.kill_timestamp = convert_zk_timestamp_to_datetime(
        pk['killmail']['killTime']
    )
    # This is temporary while we debug why some kills are coming across with no ship name
    if not pk['killmail']['victim']['shipType'] or not pk['killmail']['victim']['shipType']['name']:
        logger.error('{}-{} service - kill has no shipType or shipName. This will fail. full_response:\n{}\n\n'.format(
            pk['killID'],
            tracking_label,
            json.dumps(zk)
        ))
    tk.ship_id = pk['killmail']['victim']['shipType']['id']
    tk.ship_name = pk['killmail']['victim']['shipType']['name']
    # structure kills do not have an associated character
    if 'character' in pk['killmail']['victim']:
        tk.character_id = pk['killmail']['victim']['character']['id']
        tk.character_name = pk['killmail']['victim']['character']['name']
    tk.corporation_id = pk['killmail']['victim']['corporation']['id']
    tk.corporation_name = pk['killmail']['victim']['corporation']['name']
    # players do not have to join an alliance
    if 'alliance' in pk['killmail']['victim']:
        tk.alliance_id = pk['killmail']['victim']['alliance']['id']
        tk.alliance_name = pk['killmail']['victim']['alliance']['name']
    tk.total_value = pk['zkb']['totalValue']
    tk.system_id = pk['killmail']['solarSystem']['id']
    tk.system_name = pk['killmail']['solarSystem']['name']
    tk.more_info_href = 'https://zkillboard.com/kill/{}/'.format(pk['killID'])
    tk.full_response = json.dumps(zk)

    return tk
