from datetime import datetime
import logging

from testrattingcapitals.processors import shared_defines

TRACKING_LABEL = 'BAD_DRAGON_DEPLOYMENT'

START_TIMESTAMP = datetime(2017, 7, 22, 19, 0, 0)
END_TIMESTAMP = None  # TODO update when we move out
ESOTERIA_SYSTEM_NAMES = {  # http://evemaps.dotlan.net/region/Esoteria
    # 3WN-1T constellation
    '6EK-BV',
    'BY-MSY',
    'CZ6U-1',
    'D-PNP9',
    'E1UU-3',
    'G-YZUX',
    'P-3XVV',

    # 7ZRW-G constellation
    '111-F1',
    '6-TYRX',
    'H-T40Z',
    'IR-FDV',
    'J-RVGD',
    'NIZJ-0',
    'Q1-R7K',
    'V1ZC-S',

    # 8T-OLH constellation
    '4-OUKF',
    '5-9UXZ',
    'C9N-CC',
    'DTX8-M',
    'HAJ-DQ',
    'JAUD-V',
    'Q0OH-V',
    'X-7BIX',

    # 9D1V-O constellation
    '29YH-V',
    'DL-CDY',
    'IPX-H5',
    'LG-RO2',
    'QS-530',
    'VR-YRV',
    'X-HISR',

    # E-ILCH constellation
    'DIBH-Q',
    'DNEP-Y',
    'G-4H4C',
    'G-JC9R',
    'H-YHYM',
    'HHE5-L',
    'PE-H02',
    'YAP-TN',
    'Z-MO29',
    '02V-BK',
    'A5MT-B',
    'JD-TYH',
    'MS2-V8',
    'R-ARKN',
    'SN9S-N',

    # FY6-NK constellation
    '2R-KLH',
    '6SB-BN',
    'B1D-KU',
    'KSM-1T',
    'QFIU-K',
    'YRV-MZ',

    # JSZ-X6 constellation
    '16P-PX',
    'BZ-0GW',
    'CR-0E5',
    'WX-6UX',
    'XKZ8-H',
    'Z-Y9C3',

    # KUSW-P constellation
    'A-CJGE',
    'G2-INZ',
    'HHQ-M1',
    'HT4K-M',
    'RBW-8G',
    'VYJ-DA',
    'WAC-HW',

    # O-PQU0 constellation
    '7P-J38',
    'C-PEWN',
    'L-M6JK',
    'P9F-ZG',
    'PK-PHZ',
    'QFGB-E',
    'WT-2J9',

    # Q-2BI6 constellation
    '0-O6XF',
    'C-VZAK',
    'D-FVI7',
    'FN-GFQ',
    'NH-R5B',
    'VL7-60',

    # R2-BT6 constellation
    '450I-W',
    'A1-AUH',
    'F-UVBV',
    'OIOM-Y',
    'R-FM0G',
    'TEIZ-C',
    'V-XANH',
    'VUAC-Y',
}

logger = logging.getLogger('testrattingcapitals')


def process(zkill):
    if not isinstance(zkill, dict):
        logger.debug('? processor DEPLOYMENT_BAD_DRAGON REJECT - not dict')
        return None

    # is alliance kill
    if 'alliance' not in zkill['package']['killmail']['victim']:
        logger.debug(
            '{} processor DEPLOYMENT_BAD_DRAGON REJECT - no alliance'.format(
                zkill['package']['killID']
            )
        )
        return None

    if shared_defines.TEST_ALLIANCE_ID != zkill['package']['killmail']['victim']['alliance']['id']:
        logger.debug(
            '{} processor DEPLOYMENT_BAD_DRAGON REJECT - wrong alliance_id'.format(
                zkill['package']['killID']
            )
        )
        return None

    # is after startdate
    kill_time = datetime.strptime(zkill['package']['killmail']['killTime'], '%Y.%m.%d %H:%M:%S')
    if START_TIMESTAMP and kill_time < START_TIMESTAMP:
        logger.debug(
            '{} processor DEPLOYMENT_BAD_DRAGON REJECT - predates START_TIMESTAMP'.format(
                zkill['package']['killID']
            )
        )
        return None

    # is before enddate
    if END_TIMESTAMP and kill_time > END_TIMESTAMP:
        logger.debug(
            '{} processor DEPLOYMENT_BAD_DRAGON REJECT - postdates END_TIMESTAMP'.format(
                zkill['package']['killID']
            )
        )
        return None

    # is in esoteria
    kill_system = zkill['package']['killmail']['solarSystem']['name']
    if kill_system not in ESOTERIA_SYSTEM_NAMES:
        logger.debug(
            '{} processor DEPLOYMENT_BAD_DRAGON REJECT - system_id not in {}'.format(
                zkill['package']['killID'],
                'ESOTERIA_SYSTEM_NAMES'
            )
        )
        return None

    return TRACKING_LABEL
