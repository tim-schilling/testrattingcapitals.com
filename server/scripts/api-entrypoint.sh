#!/bin/sh

set -ex

export PYTHONPATH="/app:$PYTHONPATH"
uwsgi "uwsgi.ini"
