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
    logger.debug('start date: {}'.format(start_date.isoformat()))
    for processor in PROCESSORS:
        tracking_label = processor.TRACKING_LABEL
        db_set = tracked_kill_service.get_since(tracking_label, start_date)
        if db_set:
            if len(db_set) > 0:
                latest = db_set[0]
                cache_service.set_latest_tracked_kill_for_tracking_label(tracking_label, latest)
            cache_service.set_recent_tracked_kills_for_tracking_label(tracking_label, db_set)


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
