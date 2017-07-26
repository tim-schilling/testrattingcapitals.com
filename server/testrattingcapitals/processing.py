import logging
import os
from testrattingcapitals.processors import \
    all_processor, \
    deployment_bad_dragon_processor, \
    ratting_capital_processor, \
    vni_processor

logger = logging.getLogger('testrattingcapitals')

PROCESSORS = [
    deployment_bad_dragon_processor.process,
    ratting_capital_processor.process,
    vni_processor.process,
]

if os.getenv('PERSIST_ALL'):
    PROCESSORS.append(all_processor.process)


def process(zkill):
    labels = set()
    logger.debug('{} processing'.format(zkill['package']['killID']))
    for proc in PROCESSORS:
        proc_result = proc(zkill)
        if proc_result is not None:
            labels.add(proc_result)

    logger.info('{} processed. Labels attached: {}'.format(zkill['package']['killID'], labels or '(none)'))
    return labels
