from sqlalchemy import func

from db import Context
from schema import TrackedKill


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
            context.session.add(tracked_kill)
            context.session.commit()
