import logging

TRACKING_LABEL = 'ALL'

logger = logging.getLogger('testrattingcapitals')


def process(zkill):
    if not isinstance(zkill, dict):
        logger.debug('? processor ALL REJECT - not dict')
        return None
    logger.debug('? processor ALL ACCEPT')
    return TRACKING_LABEL
