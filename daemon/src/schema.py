from sqlalchemy import Column, DateTime, Float, Index, Integer, String, \
    Text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class TrackedKill(Base):
    """Model defining a kill.

    Various queryable fields stored at the table-field level. Full ZKillboard
    JSON object stored in field `full_response`.
    """
    __tablename__ = 'tracked_kill'

    kill_tracking_label = Column(String(255), primary_key=True)
    kill_id = Column(Integer, primary_key=True)
    kill_timestamp = Column(DateTime, nullable=False)
    ship_id = Column(Integer, nullable=False)
    ship_name = Column(String(50), nullable=False)
    character_id = Column(Integer, nullable=False)
    character_name = Column(String(255), nullable=False)
    corporation_id = Column(Integer, nullable=False)
    corporation_name = Column(String(255), nullable=False)
    alliance_id = Column(Integer)
    alliance_name = Column(String(255))
    total_value = Column(Float, nullable=False)
    system_id = Column(Integer, nullable=False)
    system_name = Column(String(50), nullable=False)
    more_info_href = Column(String(255), nullable=False)
    full_response = Column(Text, nullable=False)

    Index('idx_tracked_kill_by_label_timestamp', kill_tracking_label, kill_timestamp.desc(), kill_id, more_info_href, unique=True)
