import logging
from processors import shared_defines

TRACKING_LABEL = 'RATTING_CAPITAL'

RATTING_CAPITAL_SHIP_IDS = {
    # CARRIER
    23757,  # archon
    23911,  # thanatos
    24483,  # nidhogger
    23915,  # chimera

    # SUPERCARRIER
    23919,  # aeon
    23913,  # nyx
    22852,  # hel
    23917,  # wyvern
    3514,  # revenant
    42125,  # vendetta

    # MINING
    28606,  # orca
    28352,  # rorqual
    33687,  # rorqual ore development edition

    # FREIGHTER
    20183,  # providence
    20187,  # obelisk
    20189,  # fenrir
    20185,  # charon
    34328,  # bowhead

    # JUMP FREIGHTER
    28850,  # ark
    28848,  # anshar
    28846,  # nomad
    28844,  # rhea
},

logger = logging.getLogger('testrattingcapitals')


def process(zkill):
    if not isinstance(zkill, dict):
        logger.debug('? processor RATTING_CAPITAL REJECT - not dict')
        return None

    # is alliance kill
    if 'alliance' not in zkill['package']['killmail']['victim']:
        logger.debug(
            '{} processor RATTING_CAPITAL REJECT - no alliance'.format(
                zkill['package']['killID']
            )
        )
        return None

    if shared_defines.TEST_ALLIANCE_ID != zkill['package']['killmail']['victim']['alliance']['id']:
        logger.debug(
            '{} processor RATTING_CAPITAL REJECT - wrong alliance_id'.format(
                zkill['package']['killID']
            )
        )
        return None

    # is a ratting capital
    kill_ship_id = zkill['package']['killmail']['victim']['shipType']['id']
    if kill_ship_id not in RATTING_CAPITAL_SHIP_IDS:
        logger.debug(
            '{} processor RATTING_CAPITAL REJECT - ship_id not in RATTING_CAPITAL_SHIP_IDS'.format(
                zkill['package']['killID']
            )
        )
        return None

    return TRACKING_LABEL
