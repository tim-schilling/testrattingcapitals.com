#!/bin/sh

set -ex

export PYTHONPATH="/app:$PYTHONPATH"
alembic upgrade head
python -m "testrattingcapitals.bin.daemon"
