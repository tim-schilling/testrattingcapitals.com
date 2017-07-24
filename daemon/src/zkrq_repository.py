import logging
import os
import requests

DEFAULT_ZKRQ_URL = 'https://redisq.zkillboard.com/listen.php'

logger = logging.getLogger('testrattingcapitals')


def get(params={}, headers={}):
    logger.debug('Repository querying zkrq')
    request_headers = requests.utils.default_headers()
    request_headers.update(headers)
    return requests.get(
        os.getenv('ZKRQ_URL', DEFAULT_ZKRQ_URL),
        params=params,
        headers=headers
    )
