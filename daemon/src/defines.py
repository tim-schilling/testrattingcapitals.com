"""Application-level constants.
"""
TRACKING_LABEL_SHIP_IDS = {
    """Ship IDs to associate with a particular tracking label
    """

    'ratting_capital': [
        # CARRIER
        23757,  # archon
        23911,  # thanatos
        24483,  # nidhogger
        23915,  # chimera

        # SUPERCARRIER
        23919,  # aeon
        23913,  # nyx
        22852,  # hel
        23917,  # wyvern
        3514,  # revenant
        42125,  # vendetta

        # MINING
        28606,  # orca
        28352,  # rorqual
        33687,  # rorqual ore development edition

        # FREIGHTER
        20183,  # providence
        20187,  # obelisk
        20189,  # fenrir
        20185,  # charon
        34328,  # bowhead

        # JUMP FREIGHTER
        28850,  # ark
        28848,  # anshar
        28846,  # nomad
        28844,  # rhea
    ],
    'vni': [
        17843,  # vexor navy issue
    ],
}

DEFAULT_DB_CONNECTION_STRING = 'sqlite:///db.sqlite3'

DEFAULT_ZKRQ_URL = 'https://redisq.zkillboard.com/listen.php'
