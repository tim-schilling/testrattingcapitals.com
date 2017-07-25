import logging
import json
import os
import signal
import sys
import time

import processing
import tracked_kill_service

logger = logging.getLogger('testrattingcapitals')

TICK_RATE = int(os.getenv('TICK_RATE', '10'))

interrupt = False


def shutdown(*args, **kwargs):
    global interrupt
    logger.info('Shutting down')
    interrupt = True


def configure_logging():
    logger.setLevel(int(os.getenv('LOG_LEVEL', logging.DEBUG)))
    stdio = logging.StreamHandler()
    stdio.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(stdio)


def processing_loop(kill):
    if kill:
        # parse json to dict dict
        kill_dict = json.load(kill.full_response)
        # process dict
        labels = processing.process(kill_dict)
        for label in labels:
            tracked_kill_service.add(label, kill_dict)
    else:
        raise Exception('processing_loop called with no kill')


def main():
    global interrupt
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    configure_logging()
    logger.info('testrattingcapitals reprocessor started')

    kills = tracked_kill_service.get('ALL')

    logger.debug('Reprocessing {} kills'.format(len(kills)))
    counter = 0

    while kills:
        try:
            counter = counter + 1
            kill = kills.pop()
            logger.info('Reprocessing #{} (kill_id {})'.format(
                counter,
                kill.kill_id
            ))
            processing_loop(kill)
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
