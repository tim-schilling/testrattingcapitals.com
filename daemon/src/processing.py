import logging
from processors import \
    all_processor, \
    deployment_bad_dragon_processor, \
    ratting_capital_processor, \
    vni_processor

logger = logging.getLogger('testrattingcapitals')

PROCESSORS = [
    all_processor.process,
    deployment_bad_dragon_processor.process,
    ratting_capital_processor.process,
    vni_processor.process,
]


def process(zkill):
    logger.debug('{} processing'.format(zkill['package']['killID']))
    labels = set()
    for proc in PROCESSORS:
        proc_result = proc(zkill)
        if proc_result is not None:
            labels.add(proc_result)

    logger.info('{} processed. Labels attached: {}'.format(zkill['package']['killID'], labels))
    return labels
