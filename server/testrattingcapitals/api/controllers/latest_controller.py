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

import json
import logging
import os

from flask import jsonify
from flask_restful import Resource

from testrattingcapitals import cache_service
from testrattingcapitals.processors import (
    all_processor,
    deployment_bad_dragon_processor,
    ratting_capital_processor,
    vni_processor,
)

logger = logging.getLogger('testrattingcapitals')

PROCESSORS = [
    deployment_bad_dragon_processor,
    ratting_capital_processor,
    vni_processor,
]

if os.getenv('PERSIST_ALL'):
    PROCESSORS.append(all_processor)


class LatestController(Resource):
    def get(self):
        result = dict()
        for proc in PROCESSORS:
            kill = cache_service.get_latest_for_tracking_label(
                proc.TRACKING_LABEL
            )

            # unmarshal the inner killmail json at the edge for now
            # TODO think of a better way to deal with the 'json in the text field nonsense
            if kill and kill.full_response:
                kill.full_response = json.loads(kill.full_response)

            result[proc.TRACKING_LABEL] = {
                'kill': kill
            }
        return jsonify(result)
