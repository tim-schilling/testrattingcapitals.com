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
import logging

from testrattingcapitals.processors import shared_defines

TRACKING_LABEL = 'BAD_DRAGON_DEPLOYMENT'

START_TIMESTAMP = datetime(2017, 7, 22, 19, 0, 0)
END_TIMESTAMP = None  # TODO update when we move out
ESOTERIA_SYSTEM_IDS = {  # http://evemaps.dotlan.net/region/Esoteria
    30003098, 30003099, 30003100, 30003101, 30003102, 30003103, 30003104,
    30003105, 30003106, 30003107, 30003108, 30003109, 30003110, 30003111,
    30003112, 30003113, 30003114, 30003115, 30003116, 30003117, 30003118,
    30003119, 30003120, 30003121, 30003122, 30003123, 30003124, 30003125,
    30003126, 30003127, 30003128, 30003129, 30003130, 30003131, 30003132,
    30003133, 30003134, 30003135, 30003136, 30003137, 30003138, 30003139,
    30003140, 30003141, 30003142, 30003143, 30003144, 30003145, 30003146,
    30003147, 30003148, 30003149, 30003150, 30003151, 30003152, 30003153,
    30003154, 30003155, 30003156, 30003157, 30003158, 30003159, 30003160,
    30003161, 30003162, 30003163, 30003164, 30003165, 30003166, 30003167,
    30003168, 30003169, 30003170, 30003171, 30003172, 30003173, 30003174,
    30003175, 30003176, 30003177, 30003178, 30003179, 30003180, 30003181,
    30003182
}

logger = logging.getLogger('testrattingcapitals')


def process(zkill):
    if not isinstance(zkill, dict):
        logger.debug('? processor DEPLOYMENT_BAD_DRAGON REJECT - not dict')
        return

    # is alliance kill
    if 'alliance' not in zkill['package']['killmail']['victim']:
        logger.debug(
            '{} processor DEPLOYMENT_BAD_DRAGON REJECT - no alliance'.format(
                zkill['package']['killID']
            )
        )
        return

    if shared_defines.TEST_ALLIANCE_ID != zkill['package']['killmail']['victim']['alliance']['id']:
        logger.debug(
            '{} processor DEPLOYMENT_BAD_DRAGON REJECT - wrong alliance_id'.format(
                zkill['package']['killID']
            )
        )
        return

    # is after startdate
    kill_time = datetime.strptime(zkill['package']['killmail']['killTime'], '%Y.%m.%d %H:%M:%S')
    if START_TIMESTAMP and kill_time < START_TIMESTAMP:
        logger.debug(
            '{} processor DEPLOYMENT_BAD_DRAGON REJECT - predates START_TIMESTAMP'.format(
                zkill['package']['killID']
            )
        )
        return

    # is before enddate
    if END_TIMESTAMP and kill_time > END_TIMESTAMP:
        logger.debug(
            '{} processor DEPLOYMENT_BAD_DRAGON REJECT - postdates END_TIMESTAMP'.format(
                zkill['package']['killID']
            )
        )
        return

    # is in esoteria
    kill_system = zkill['package']['killmail']['solarSystem']['id']
    if kill_system not in ESOTERIA_SYSTEM_IDS:
        logger.debug(
            '{} processor DEPLOYMENT_BAD_DRAGON REJECT - system_id not in {}'.format(
                zkill['package']['killID'],
                'ESOTERIA_SYSTEM_IDS'
            )
        )
        return

    return TRACKING_LABEL
