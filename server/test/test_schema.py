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

from datetime import datetime
from testrattingcapitals.schema import TrackedKill as Unit


def test_to_from_json():
    result = Unit.to_json(None)
    assert result is None

    result = Unit.from_json(None)
    assert result is None

    a_kill = Unit(
        kill_id=50,
        kill_timestamp=datetime(2017, 7, 30),
        kill_tracking_label='UNITTEST'
    )

    as_json = Unit.to_json(a_kill)
    assert isinstance(as_json, str)
    assert a_kill.kill_timestamp.isoformat() in as_json
    assert '50' in as_json
    assert 'UNITTEST' in as_json

    back_again = Unit.from_json(as_json)
    assert isinstance(back_again, Unit)
    assert a_kill.kill_id == back_again.kill_id
    assert a_kill.kill_timestamp == back_again.kill_timestamp
    assert a_kill.kill_tracking_label == back_again.kill_tracking_label
