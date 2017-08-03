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


def register(app):
    if not isinstance(app, Flask):
        raise TypeError('app')

    for middleware in middleware_modules:
        if hasattr(middleware, 'before_first_request'):
            app.before_first_request(middleware.before_first_request)
        if hasattr(middleware, 'before_request'):
            app.before_request(middleware.before_request)
        if hasattr(middleware, 'teardown_request'):
            app.teardown_request(middleware.teardown_request)
        if hasattr(middleware, 'after_request'):
            app.after_request(middleware.after_request)

    return app
