import logging
import os
import requests

DEFAULT_ZKRQ_URL = 'https://redisq.zkillboard.com/listen.php'

logger = logging.getLogger('testrattingcapitals')


def get(params={}):
    logger.debug('Repository querying zkrq')
    return requests.get(
        os.getenv('ZKRQ_URL', DEFAULT_ZKRQ_URL),
        params=params
    )
