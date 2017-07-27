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
            '{} processor VNI REJECT - ship_id not equal VNI_SHIP_ID'.format(
                zkill['package']['killID']
            )
        )
        return None

    return TRACKING_LABEL
