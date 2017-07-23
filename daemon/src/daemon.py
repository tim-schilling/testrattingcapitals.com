from datetime import datetime
from schema import TrackedKill

import tracked_kill_repository

num = 1

tracked_kill_repository.add(
    TrackedKill(
        kill_tracking_label='test',
        kill_id=num,
        kill_timestamp=datetime.utcnow(),
        ship_id=num,
        ship_name='test',
        character_id=num,
        character_name='test',
        corporation_id=num,
        corporation_name='test',
        total_value=num,
        system_id=num,
        system_name='test',
        more_info_href='test',
        full_response='test',
    )
)
