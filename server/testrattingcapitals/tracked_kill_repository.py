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

import logging
from sqlalchemy import func

from testrattingcapitals.db import Context
from testrattingcapitals.schema import TrackedKill

logger = logging.getLogger('testrattingcapitals')


def add(tracked_kill):
    """Add a tracked_kill record to the db context.

    If the record already exists, do not overwrite. This lets us run multiple
    daemon instances somewhat safely.

    Note that this isn't a fullproof solution to race conditions. Our data is
    just simple and static enough that transaction-level safety is good enough.
    """
    with Context() as context:
        """sqlalchemy doesn't support upsert, so we're stuck with two round
        trips for insert safety.
        """
        existing = context.session.query(func.count(TrackedKill.kill_id)).filter(
            TrackedKill.kill_tracking_label == tracked_kill.kill_tracking_label,
            TrackedKill.kill_id == tracked_kill.kill_id
        ).scalar()
        if existing == 0:
            logger.debug('{}-{} not in persistent storage. Writing.'.format(tracked_kill.kill_id, tracked_kill.kill_tracking_label))
            context.session.add(tracked_kill)
            context.session.commit()
        else:
            logger.debug('{}-{} already in persistent storage. Discarding.'.format(tracked_kill.kill_id, tracked_kill.kill_tracking_label))


def get(tracking_label):
    """Retrieve all records, optionally filtering by tracking_label.
    """
    with Context() as context:
        if tracking_label:
            return context.session.query(TrackedKill).filter(
                TrackedKill.kill_tracking_label == tracking_label
            ).all()
        else:
            return context.session.query(TrackedKill).all()


def get_since(tracking_label, start_date):
    """Retrieve all kills for a tracking_label since start_date.
    """
    logger.debug('{}-{} repository querying get_since'.format(
        tracking_label,
        start_date.isoformat()
    ))
    with Context() as context:
        return context.session.query(TrackedKill).filter(
            TrackedKill.kill_tracking_label == tracking_label,
            TrackedKill.kill_timestamp >= start_date
        ).order_by(
            TrackedKill.kill_timestamp.desc()
        ).all()
