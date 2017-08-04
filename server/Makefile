#!/usr/bin/make -f

# Shamelessly based off @rw_grim's python makefile configuration, without
# whom my knowledge of make and shell scripting would still consist of tears
# and therapy

REQUIREMENTS = \
	requirements-api.txt \
	requirements-cacher.txt \
	requirements-daemon.txt \
	requirements-reprocessor.txt \
	requirements-testing.txt \

DB_MIGRATION_COMMAND ?= alembic upgrade head
DB_PATH ?= db.sqlite3
DB_CONNECTION_STRING ?= sqlite:///$(DB_PATH)

FLASK_HOST ?= 127.0.0.1
FLASK_PORT ?= 8080
CORS_ALLOWED_ORIGINS ?= http://localhost:8080

MIGRATIONS_DIR ?= migrations

PYTHON_BIN ?= python3
PYTHONPATH ?= $(shell pwd)

TEST_DIR ?= test
TEST_OPTIONS ?= -vv --junitxml=junit.xml --cov-report term-missing --cov=testrattingcapitals

VENV_BIN ?= virtualenv
VENV_PATH ?= venv
VENV_ACTIVATE = $(VENV_PATH)/bin/activate

.PHONY: all migrate run virtualenv clean clean-pyc 

all: lint check migrate

clean: clean-pyc
	rm -rf build dist
	rm -rf *.egg-info
	rm -f junit.xml
	rm -rf $(VENV_PATH)
	rm -f $(DB_PATH)

clean-pyc:
	find $(PYTHONPATH) $(MIGRATIONS_DIR) -iname "*.pyc" -type f | xargs -n 10 rm -f
	find $(PYTHONPATH) $(MIGRATIONS_DIR) -name __pycache__ -type d | xargs -n 10 rm -rf

virtualenv: $(VENV_ACTIVATE)

$(VENV_ACTIVATE): $(REQUIREMENTS)
	test -f $(VENV_PATH)/bin/$(PYTHON_BIN) || $(VENV_BIN) --no-site-packages --python=$(PYTHON_BIN) $(VENV_PATH)
	. $(VENV_ACTIVATE); pip install -U pip
	. $(VENV_ACTIVATE); echo $(REQUIREMENTS) | xargs -n 1 pip install -r
	touch $@

lint: virtualenv
	. $(VENV_ACTIVATE) ; flake8 --config tox.ini --statistics --count $(LINT_OPTIONS)

check: virtualenv lint $(EXTRA_CHECKS)
	. $(VENV_ACTIVATE) ; PYTHONPATH=$(PYTHONPATH) py.test $(TEST_OPTIONS) --color=auto $(TEST_DIR)

migrate: virtualenv
	. $(VENV_ACTIVATE) ; PYTHONPATH=$(PYTHONPATH) $(DB_MIGRATION_COMMAND)

run-daemon: virtualenv migrate
	. $(VENV_ACTIVATE) ; TICK_RATE=1 PERSIST_ALL=1 python -m "testrattingcapitals.bin.daemon"

run-reprocessor: virtualenv migrate
	. $(VENV_ACTIVATE) ; TICK_RATE=1 PERSIST_ALL=1 python -m "testrattingcapitals.bin.reprocessor"

run-cacher: virtualenv migrate
	. $(VENV_ACTIVATE) ; TICK_RATE=1 PERSIST_ALL=1 python -m "testrattingcapitals.bin.cacher"

run-api: virtualenv migrate
	. $(VENV_ACTIVATE) ; PERSIST_ALL=1 FLASK_DEBUG=1 FLASK_APP="testrattingcapitals/bin/api.py" CORS_ALLOWED_ORIGINS=$(CORS_ALLOWED_ORIGINS) flask run --host=$(FLASK_HOST) --port=$(FLASK_PORT)

run-api-uwsgi: virtualenv migrate
	. $(VENV_ACTIVATE) ; PERSIST_ALL=1 uwsgi "uwsgi.ini"
