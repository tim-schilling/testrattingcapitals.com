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

from flask import Flask
from testrattingcapitals.api.middlewares import cors

middleware_modules = [
    cors
]


MIDDLEWARE_METHODS = [
  'before_first_request',
  'before_request',
  'teardown_request',
  'after_request',
]
  
def register(app):
    if not isinstance(app, Flask):
        raise TypeError('app')

    for middleware in middleware_modules:
        for method_name in MIDDLEWARE_METHODS:
            if hasattr(middleware, method_name):
                getattr(app, method_name)(getattr(middleware, method_name))

    return app
