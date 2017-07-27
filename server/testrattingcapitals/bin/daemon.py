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

import logging
import os
import signal
import sys
import time

from testrattingcapitals import processing, tracked_kill_service, zkrq_service

logger = logging.getLogger('testrattingcapitals')

TICK_RATE = int(os.getenv('TICK_RATE', '10'))
ZKRQ_QUEUE_ID = os.getenv('ZKRQ_QUEUE_ID')
ZKRQ_TTW = os.getenv('ZKRQ_TTW')

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
    kill = zkrq_service.get(ZKRQ_QUEUE_ID, ZKRQ_TTW)
    if kill:
        labels = processing.process(kill)
        for label in labels:
            tracked_kill_service.add(label, kill)


def main():
    global interrupt
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    configure_logging()
    logger.info('testrattingcapitals daemon started')

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
