from processors import shared_defines

TRACKING_LABEL = 'VNI'

VNI_SHIP_ID = 17843,  # vexor navy issue


def process(zkill):
    if not isinstance(zkill, dict):
        return None

    # is alliance kill
    if 'alliance' not in zkill['package']['killmail']['victim']:
        return None

    if shared_defines.TEST_ALLIANCE_ID != zkill['package']['killmail']['victim']['alliance']['id']:
        return None

    # is a VNI
    kill_ship_id = zkill['package']['killmail']['victim']['shipType']['id']
    if kill_ship_id != VNI_SHIP_ID:
        return None

    return TRACKING_LABEL
