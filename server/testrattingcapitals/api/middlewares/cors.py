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

import os


def after_request(response):
    if not response or not hasattr(response, 'headers'):
        return response

    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS
    # https://fetch.spec.whatwg.org/#cors-protocol

    cors_headers = {
        'Access-Control-Allow-Origin': os.getenv('CORS_ALLOWED_ORIGINS'),
        'Access-Control-Expose-Headers': os.getenv('CORS_EXPOSE_HEADERS'),
        'Access-Control-Max-Age': os.getenv('CORS_MAX_AGE'),
        'Access-Control-Allow-Credentials': os.getenv('CORS_ALLOW_CREDENTIALS'),
        'Access-Control-Allow-Methods': os.getenv('CORS_ALLOW_METHODS'),
    }

    for key, value in cors_headers.items():
        if key == 'Access-Control-Allow-Credentials' and value != 'true':
            continue

        if value:
            response.headers[key] = value

    return response
