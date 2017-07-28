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
import json
import pytest

from testrattingcapitals import tracked_kill_service as unit
from testrattingcapitals.schema import TrackedKill


def test_validate_tracking_label():
    with pytest.raises(TypeError):
        unit.validate_tracking_label(1234)

    with pytest.raises(TypeError):
        unit.validate_tracking_label(None)

    with pytest.raises(ValueError):
        unit.validate_tracking_label('')

    unit.validate_tracking_label('valid')


def test_validate_zk_response():
    with pytest.raises(TypeError):
        unit.validate_zk_response(None)

    with pytest.raises(TypeError):
        unit.validate_zk_response('blah')

    unit.validate_zk_response({})


def test_convert_zk_timestamp_to_datetime():
    input_assertion_tuples = [
        ('2017.07.23 01:08:58', datetime(2017, 7, 23, 1, 8, 58),),
        (None, None, ),
    ]

    for t in input_assertion_tuples:
        result = unit.convert_zk_timestamp_to_datetime(t[0])
        assert t[1] == result


def test_convert_zk_response_to_tracked_kill():
    input_tracking_label = 'unittest'

    # example_zkill_response_body.json
    input_zk_response = json.loads(
        """{"package":{"killID":63639452,"killmail":{"solarSystem":{"id_str":"30003699","href":"https://crest-tq.eveonline.com/solarsystems/30003699/","id":30003699,"name":"MPPA-A"},"killID":63639452,"killTime":"2017.07.23 01:08:58","attackers":[{"alliance":{"id_str":"1900696668","href":"https://crest-tq.eveonline.com/alliances/1900696668/","id":1900696668,"name":"The Initiative.","icon":{"href":"http://imageserver.eveonline.com/Alliance/1900696668_128.png"}},"shipType":{"id_str":"670","href":"https://crest-tq.eveonline.com/inventory/types/670/","id":670,"name":"Capsule","icon":{"href":"http://imageserver.eveonline.com/Type/670_128.png"}},"corporation":{"id_str":"98114328","href":"https://crest-tq.eveonline.com/corporations/98114328/","id":98114328,"name":"Fweddit","icon":{"href":"http://imageserver.eveonline.com/Corporation/98114328_128.png"}},"character":{"id_str":"1242179382","href":"https://crest-tq.eveonline.com/characters/1242179382/","id":1242179382,"name":"Tallitar","icon":{"href":"http://imageserver.eveonline.com/Character/1242179382_128.jpg"}},"damageDone_str":"211","weaponType":{"id_str":"27920","href":"https://crest-tq.eveonline.com/inventory/types/27920/","id":27920,"name":"Electron Bomb","icon":{"href":"http://imageserver.eveonline.com/Type/27920_128.png"}},"finalBlow":true,"securityStatus":5,"damageDone":211}],"attackerCount":1,"victim":{"alliance":{"id_str":"99005338","href":"https://crest-tq.eveonline.com/alliances/99005338/","id":99005338,"name":"Pandemic Horde","icon":{"href":"http://imageserver.eveonline.com/Alliance/99005338_128.png"}},"damageTaken":211,"items":[],"damageTaken_str":"211","character":{"id_str":"1942609699","href":"https://crest-tq.eveonline.com/characters/1942609699/","id":1942609699,"name":"Doug Widereamer","icon":{"href":"http://imageserver.eveonline.com/Character/1942609699_128.jpg"}},"shipType":{"id_str":"670","href":"https://crest-tq.eveonline.com/inventory/types/670/","id":670,"name":"Capsule","icon":{"href":"http://imageserver.eveonline.com/Type/670_128.png"}},"corporation":{"id_str":"98388312","href":"https://crest-tq.eveonline.com/corporations/98388312/","id":98388312,"name":"Pandemic Horde Inc.","icon":{"href":"http://imageserver.eveonline.com/Corporation/98388312_128.png"}},"position":{"y":-169999008300.3,"x":-34213667699.793,"z":343132038395.88}},"killID_str":"63639452","attackerCount_str":"1","war":{"href":"https://crest-tq.eveonline.com/wars/0/","id":0,"id_str":"0"}},"zkb":{"locationID":40234287,"hash":"4e2ef55e655f5f23dd73a83608405d1825b8398a","fittedValue":10000,"totalValue":10000,"points":1,"npc":false,"href":"https://crest-tq.eveonline.com/killmails/63639452/4e2ef55e655f5f23dd73a83608405d1825b8398a/"}}}""" # NOQA
    )

    result = unit.convert_zk_response_to_tracked_kill(input_tracking_label, input_zk_response)
    assert isinstance(result, TrackedKill)
    assert input_tracking_label == result.kill_tracking_label
    assert 63639452 == result.kill_id
    assert datetime(2017, 7, 23, 1, 8, 58) == result.kill_timestamp
    assert 670 == result.ship_id
    assert 1942609699 == result.character_id
    assert 98388312 == result.corporation_id
    assert 99005338 == result.alliance_id
    assert 10000 == result.total_value
    assert 30003699 == result.system_id
    assert 'https://zkillboard.com/kill/63639452/' == result.more_info_href
    assert json.dumps(input_zk_response) == result.full_response

    # deprecated fields should be null where possible, otherwise default value for type
    assert result.character_name is None
    assert '' == result.corporation_name
    assert result.alliance_name is None
    assert '' == result.ship_name
    assert '' == result.system_name


def test_validate_start_date():
    with pytest.raises(TypeError):
        unit.validate_start_date(None)
    unit.validate_start_date(datetime(2017, 1, 1))
