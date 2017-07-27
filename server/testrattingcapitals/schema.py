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
    ship_name = Column(String(50), nullable=False, default='')  # deprecated
    character_id = Column(Integer)
    character_name = Column(String(255))  # deprecated
    corporation_id = Column(Integer, nullable=False)
    corporation_name = Column(String(255), nullable=False, default='')  # deprecated
    alliance_id = Column(Integer)
    alliance_name = Column(String(255))  # deprecated
    total_value = Column(Float, nullable=False)
    system_id = Column(Integer, nullable=False)
    system_name = Column(String(50), nullable=False, default='')  # deprecated
    more_info_href = Column(String(255), nullable=False)
    full_response = Column(Text, nullable=False)

    Index('idx_tracked_kill_by_label_timestamp', kill_tracking_label, kill_timestamp.desc(), kill_id, more_info_href, unique=True)


class EveItem(Base):
    """Model defining any item in the game.

    Loaded from CCP database dumps. See: https://developers.eveonline.com/resource/resources.
    """
    __tablename__ = 'eve_item'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=True)


class EveSolarSystem(Base):
    """Model defining an EVE Online solar system.

    Loaded from CCP database dumps. See: https://developers.eveonline.com/resource/resources.
    """
    __tablename__ = 'eve_system'

    id = Column(Integer, primary_key=True)
    constellation_id = Column(Integer, nullable=True)
    region_id = Column(Integer, nullable=True)
    name = Column(String(50), nullable=True)
