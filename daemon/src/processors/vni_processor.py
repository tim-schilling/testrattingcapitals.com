import logging
from processors import shared_defines

TRACKING_LABEL = 'VNI'

VNI_SHIP_ID = 17843  # vexor navy issue

logger = logging.getLogger('testrattingcapitals')


def process(zkill):
    if not isinstance(zkill, dict):
        logger.debug('? processor VNI REJECT - not dict')
        return None

    # is alliance kill
    if 'alliance' not in zkill['package']['killmail']['victim']:
        logger.debug(
            '{} processor VNI REJECT - no alliance'.format(
                zkill['package']['killID']
            )
        )
        return None

    if shared_defines.TEST_ALLIANCE_ID != zkill['package']['killmail']['victim']['alliance']['id']:
        logger.debug(
            '{} processor VNI REJECT - wrong alliance_id'.format(
                zkill['package']['killID']
            )
        )
        return None

    # is a VNI
    kill_ship_id = zkill['package']['killmail']['victim']['shipType']['id']
    if kill_ship_id != VNI_SHIP_ID:
        logger.debug(
            '{} processor RATTING_CAPITAL REJECT - ship_id not equal VNI_SHIP_ID'.format(
                zkill['package']['killID']
            )
        )
        return None

    return TRACKING_LABEL
