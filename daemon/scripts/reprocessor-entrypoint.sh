#!/bin/sh

set -ex

export PYTHONPATH="/app/src:$PYTHONPATH"
alembic upgrade head
python /app/src/reprocessor.py
