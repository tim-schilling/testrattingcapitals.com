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

from testrattingcapitals.processors import shared_defines

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
}

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
