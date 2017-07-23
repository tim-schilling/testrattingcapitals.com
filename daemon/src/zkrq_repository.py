import os
import requests

DEFAULT_ZKRQ_URL = 'https://redisq.zkillboard.com/listen.php'


def get(params={}):
    return requests.get(
        os.getenv('ZKRQ_URL', DEFAULT_ZKRQ_URL),
        params=params
    )
