import os
import requests

import defines


def get(params={}):
    return requests.get(
        os.getenv('ZKRQ_URL', defines.DEFAULT_ZKRQ_URL),
        params=params
    )
