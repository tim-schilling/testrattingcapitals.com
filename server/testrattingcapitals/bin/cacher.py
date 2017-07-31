#!/usr/bin/env python3
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
import os
import signal
import sys
import time
from testrattingcapitals import cache_service, tracked_kill_service
from testrattingcapitals.processors import \
    all_processor, \
    deployment_bad_dragon_processor, \
    ratting_capital_processor, \
    vni_processor

logger = logging.getLogger('testrattingcapitals')

PROCESSORS = [
    deployment_bad_dragon_processor,
    ratting_capital_processor,
    vni_processor,
]

if os.getenv('PERSIST_ALL'):
    PROCESSORS.append(all_processor)
TICK_RATE = int(os.getenv('TICK_RATE', '10'))

interrupt = False


def shutdown(*args, **kwargs):
    global interrupt
    logger.info('Shutting down')
    interrupt = True


def configure_logging():
    logger.setLevel(int(os.getenv('LOG_LEVEL', logging.DEBUG)))
    stdio = logging.StreamHandler(sys.stdout)
    stdio.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(stdio)


def processing_loop():
    logger.debug('Processing loop tick')
    start_date = datetime.utcnow() - timedelta(days=30)
    for processor in PROCESSORS:
        logger.debug('cacher retrieving kills for {}'.format(processor.TRACKING_LABEL))
        kills = tracked_kill_service.get_since(processor.TRACKING_LABEL, start_date)
        logger.debug('cacher caching for {}'.format(processor.TRACKING_LABEL))
        cache_service.set_for_tracking_label(processor.TRACKING_LABEL, kills)
        logger.debug('cacher expiring for {}'.format(processor.TRACKING_LABEL))
        cache_service.expire_recents_for_label(processor.TRACKING_LABEL, start_date)


def main():
    global interrupt
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    configure_logging()
    logger.info('testrattingcapitals cacher started')

    while True:
        try:
            processing_loop()
        except:
            # TODO exponential fallback
            logger.exception('unhandled exception')
        if TICK_RATE > 0:
            for i in range(TICK_RATE * 4):
                time.sleep(0.25)
                if interrupt:
                    sys.exit(0)
        else:
            if interrupt:
                sys.exit(0)


if __name__ == '__main__':
    main()
