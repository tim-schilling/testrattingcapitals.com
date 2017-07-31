#!/bin/sh

set -ex

export PYTHONPATH="/app:$PYTHONPATH"
python -m "testrattingcapitals.bin.cacher"
