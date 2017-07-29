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
import os
from testrattingcapitals.processors import \
    all_processor, \
    deployment_bad_dragon_processor, \
    ratting_capital_processor, \
    vni_processor

logger = logging.getLogger('testrattingcapitals')

PROCESSORS = [
    deployment_bad_dragon_processor.process,
    ratting_capital_processor.process,
    vni_processor.process,
]

if os.getenv('PERSIST_ALL'):
    PROCESSORS.append(all_processor.process)


def process(zkill):
    labels = set()
    logger.debug('{} processing'.format(zkill['package']['killID']))
    for proc in PROCESSORS:
        proc_result = proc(zkill)
        if proc_result is not None:
            labels.add(proc_result)

    logger.debug('{} processed. Labels attached: {}'.format(zkill['package']['killID'], labels or '(none)'))
    return labels
